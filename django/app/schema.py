import graphene
from graphene_django.types import DjangoObjectType
from app.models import JobPost, Application




#GraphQL type for a JobPost
class JobPostType(DjangoObjectType):
    class Meta:
        model = JobPost
        fields = (
            "id",
            "title",
            "description",
            "company",
            "location",
            "salary",
            "posted_at",
            "is_active",
        )


#GraphQL type for a JobApplication
class ApplicationType(DjangoObjectType):
    class Meta:
        model = Application
        fields = (
            "id",
            "job_post",
            "applicant_name",
            "applicant_email",
            "resume",
            "applied_at",
        )


# Queries for fetching JobPost and Application data
class Query(graphene.ObjectType):
    all_job_posts = graphene.List(JobPostType)
    job_post_by_id = graphene.Field(JobPostType, id=graphene.Int(required=True))
    all_applications = graphene.List(ApplicationType)
    applications_by_job = graphene.List(ApplicationType, job_id=graphene.Int(required=True))

    def resolve_all_job_posts(self, info):
        return JobPost.objects.filter(is_active=True)

    def resolve_job_post_by_id(self, info, id):
        try:
            return JobPost.objects.get(id=id, is_active=True)
        except JobPost.DoesNotExist:
            return None

    def resolve_applications_by_job(self, info, job_id):
        try:
            job_post = JobPost.objects.get(id=job_id, is_active=True)
            return job_post.applications.all()
        except JobPost.DoesNotExist:
            return []
        
    def resolve_all_applications(self, info):
        return Application.objects.all()






# Creating JobPost and Application
class CreateJobPost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        company = graphene.String(required=True)
        location = graphene.String(required=True)
        salary = graphene.Float(required=False)

    job_post = graphene.Field(JobPostType)

    def mutate(self, info, title, description, company, location, salary=None):
        
        job_post = JobPost(
            title=title,
            description=description,
            company=company,
            location=location,
            salary= salary,
        )
        job_post.save()
        return CreateJobPost(job_post=job_post)





class CreateApplication(graphene.Mutation):
    class Arguments:
        job_id = graphene.Int(required=True)
        applicant_name = graphene.String(required=True)
        applicant_email = graphene.String(required=True)
        resume = graphene.String()  # update for file handling

    application = graphene.Field(ApplicationType)

    def mutate(self, info, job_id, applicant_name, applicant_email, resume=None):
        try:
            job_post = JobPost.objects.get(id=job_id, is_active=True)
            application = Application(
                job_post=job_post,
                applicant_name=applicant_name,
                applicant_email=applicant_email,
                resume=resume,
            )
            application.save()
            return CreateApplication(application=application)
        except JobPost.DoesNotExist:
            raise Exception("JobPost does not exist or is not active.")


# Deleting stuff

class DeleteJobPost(graphene.Mutation):
    class Arguments:
        job_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, job_id):
        try:
            job_post = JobPost.objects.get(id=job_id)
            job_post.delete()
            return DeleteJobPost(success=True)
        except JobPost.DoesNotExist:
            raise Exception("JobPost with the given ID does not exist.")
        

class DeleteApplication(graphene.Mutation):
    class Arguments:
        application_id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, application_id):
        try:
            application = Application.objects.get(id=application_id)
            application.delete()
            return DeleteApplication(success=True)
        except Application.DoesNotExist:
            raise Exception("Application with the given ID does not exist.")
        



# Mutation class
class Mutation(graphene.ObjectType):
    create_job_post = CreateJobPost.Field()
    create_application = CreateApplication.Field()
    delete_job_post = DeleteJobPost.Field()
    delete_application = DeleteApplication.Field()



# Schema definition
schema = graphene.Schema(query=Query, mutation=Mutation)

