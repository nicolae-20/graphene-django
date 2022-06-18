from graphene import DateTime, Int, List, Field, String
from datetime import datetime
from django.contrib.auth.models import User, Group
from graphql import GraphQLError
from .models import Instructor, Cohort, Bootcamp, Role, Topic
from graphene_django import DjangoListField, DjangoObjectType
from graphene_django_crud.types import resolver_hints, DjangoCRUDObjectType
import graphene


class UserType(DjangoCRUDObjectType):
    class Meta:
        model = User
        exclude_fields = ("password")
        input_exclude_fields = ("last_login", "date_joined")

    full_name = graphene.String()
    
    
    @resolver_hints(
        only=["first_name", "last_name"]
    )
    @staticmethod
    def resolve_full_name(parent, info, **kwargs):
        return parent.get_full_name()
    
    
    @classmethod
    def get_queryset(cls, parent, info, **kwargs):
            if info.context.user.is_authenticated:
                return User.objects.all()
            else:
                return User.objects.all()
    
    
    @classmethod
    def mutate(cls, parent, info, instance, data, *args, **kwargs):
        if not info.context.user.is_staff:
           raise GraphQLError('fara permisiune, doar membrii staff')
       
        if not info.context.user.is_authenticated:
            raise GraphQLError('neautorizat, trebuie sa te loghezi')
       
        if "password" in data.keys():
           instance.set_password(data.pop("password"))
        return super().mutate(parent, info, instance, data, *args, **kwargs)

    @classmethod
    def create(cls, parent, info, instance, data, *args, **kwargs):
        if not info.context.user.has_perm("add_user"):
            raise GraphQLError('neautorizat, trebuie sa ai permisiunea add_user')
        return super().create(parent, info, instance, data, *args, **kwargs)
    
    @classmethod
    def update(cls, parent, info, instance, data, *args, **kwargs):
        if not info.context.user.has_perm("change_user"):
            raise GraphQLError('neautorizat, trebuie sa ai permisiunea change_user')
        return super().update(parent, info, instance, data, *args, **kwargs)
    
    @classmethod
    def delete(cls, parent, info, instance, data, *args, **kwargs):
        if not info.context.user.has_perm("delete_user"):
            raise GraphQLError('neautorizat, trebuie sa ai permisiunea delete_user')
        return super().delete(parent, info, instance, data, *args, **kwargs)
    
    
class GroupType(DjangoCRUDObjectType):
    class Meta:
        model = Group
                  
        
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

class DeleteInstructor(graphene.Mutation):
    ok = graphene.Boolean()
    
    class Arguments:
        id = graphene.ID()
        
    @classmethod
    def mutate(cls, root, info, **kwargs):
        obj = Instructor.objects.get(pk=kwargs["id"])
        obj.delete()
        return cls(ok=True)
    
class InstructorMutation(object):
    delete_user = DeleteInstructor.Field()

class Mutation(graphene.ObjectType):
    create_instructor = CreateInstructor.Field() 
    delete_instructor = DeleteInstructor.Field()
    
    user_create = UserType.CreatedField()
    user_update = UserType.UpdatedField()
    user_delete = UserType.DeletedField()
    
    group_create = GroupType.CreatedField()
    group_update = GroupType.UpdatedField()
    group_delete = GroupType.DeletedField()
    

class Subscription(graphene.ObjectType):
    
    user_create = UserType.CreatedField()
    user_update = UserType.UpdatedField()
    user_delete = UserType.DeletedField()
    
    group_create = GroupType.CreatedField()
    group_update = GroupType.UpdatedField()
    group_delete = GroupType.DeletedField()
          

from .schema import UserType, GroupType

UserType.generate_signals()
GroupType.generate_signals()


class Query(object):
    me = graphene.Field(UserType)
    user = UserType.ReadField()
    users = UserType.BatchReadField()
    
    group = GroupType.ReadField()
    groups = GroupType.BatchReadField()
    
    def resolve_me(parent, info, **kwargs):
        if not info.context.user.is_authenticated:
            return None
        else:
            return info.context.user
        
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