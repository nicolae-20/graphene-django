from django.contrib import admin


from django.contrib import admin

from .models import Instructor, Bootcamp, Cohort, Role, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    pass


class CohortInline(admin.StackedInline):
    model = Cohort


@admin.register(Bootcamp)
class BootcampAdmin(admin.ModelAdmin):
    inlines = (CohortInline, )


class RoleInline(admin.StackedInline):
    model = Role


@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    inlines = (RoleInline, )