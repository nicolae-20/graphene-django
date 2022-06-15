from graphene import DateTime, Int, List, Field, String
from datetime import datetime
from .models import Instructor, Cohort, Bootcamp, Role, Topic
from graphene_django import DjangoListField, DjangoObjectType
import graphene


class BootcampType(DjangoObjectType):
    class Meta:
        model = Bootcamp


class InstructorType(DjangoObjectType):
    class Meta:
        model = Instructor


class CohortType(DjangoObjectType):
    class Meta:
        model = Cohort


class RoleType(DjangoObjectType):
    class Meta:
        model = Role
        

class TopicType(DjangoObjectType):
    class Meta:
        model = Topic


class CreateInstructor(graphene.Mutation):
    name = graphene.String()
    name_ro = graphene.String()
    bio = graphene.String()
    bio_ro = graphene.String()

    class Arguments:
        name = graphene.String()
        name_ro = graphene.String()
        bio = graphene.String()
        bio_ro = graphene.String()

    def mutate(self, info, name, name_ro, bio, bio_ro):
        instructor = Instructor(
            name = name,
            name_ro = name_ro,
            bio = bio,
            bio_ro = bio_ro
        )
        instructor.save()
        
        return CreateInstructor(
            name = instructor.name,
            name_ro = instructor.name_ro,
            bio = instructor.bio,
            bio_ro = instructor.bio_ro,
        )
        

class Mutation(graphene.ObjectType):
    create_instructor = CreateInstructor.Field()       


class Query(object):
    date = DateTime()
    bootcamps = DjangoListField(BootcampType)
    cohorts = DjangoListField(CohortType)
    topics = DjangoListField(TopicType)
    instructors = List(InstructorType)
    instructor = Field(InstructorType, id=Int(), name=String())
    
    def resolve_date(self, info):
        return datetime.now().date()
    
    def resolve_instructors(self, info):
        return Instructor.objects.all()
    
    def resolve_instructor(self, info, id=None, name=None):
        if id is not None:
            return Instructor.objects.get(pk=id)
        if name is not None:
            return Instructor.objects.get(name=name)
        return None
        
        
class Mutation(graphene.ObjectType):
    create_instructor = CreateInstructor.Field()