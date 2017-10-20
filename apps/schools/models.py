from django.conf import settings
from django.db import models
from apps.accounts.models import Organization
from .constants import DAY_OF_THE_WEEK


class School(models.Model):
    """
    Represents a school
    """
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, related_name='schools')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    """
    Represents a school member of staff
    """
    bio = models.TextField(default='', blank=True, null=True)
    school = models.ForeignKey('School', related_name='staff')
    role = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='staff_profile')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class Student(models.Model):
    """
    Represents a student of school
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='student_profile')
    school = models.ForeignKey('School', related_name='students')

    def __str__(self):
        return self.user


class Parent(models.Model):
    """
    Represents a parent of a student
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='parent_profile')
    students = models.ManyToManyField('Student')

    def __str__(self):
        return self.user


class Class(models.Model):
    """
    Represents a group of students
    """
    name = models.CharField(max_length=255)
    students = models.ManyToManyField('Student')
    academic_year = models.PositiveIntegerField()
    school = models.ForeignKey('School', related_name='classes')
    supervisor = models.ForeignKey('Staff', related_name='classes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ClassAttendance(models.Model):
    """
    Student Class Attendance
    """
    student = models.ForeignKey('Student')
    student_class = models.ForeignKey('Class')
    remarks = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Subject(models.Model):
    """
    Represents a subject a student can take
    """
    name = models.CharField(max_length=255)
    school = models.ForeignKey('School', related_name='subjects')

    def __str__(self):
        return self.name


class SubjectClass(models.Model):
    """
    Represents a physical class students attend
    """
    subject = models.ForeignKey('Subject')
    time = models.TimeField()
    day = models.CharField(max_length=2, choices=DAY_OF_THE_WEEK)
    students = models.ManyToManyField('Student', related_name='classes')
    instructor = models.ForeignKey('Staff')
    location = models.CharField(max_length=255)

    class Meta:
        unique_together = ('subject', 'time', 'day', )

    def __str__(self):
        return "{} {}".format(self.subject.name, self.time)


class AssessmentType(models.Model):
    """
    Represents a type of assessment
    """
    name = models.CharField(max_length=255, unique=True)


class Assessment(models.Model):
    """
    Represents an assessment for a subject
    """
    title = models.TextField()
    total_marks = models.PositiveIntegerField()
    assessment_type = models.ForeignKey('AssessmentType')
    subject = models.ForeignKey('Subject')
    visible = models.BooleanField(default=False)
    due_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Submission(models.Model):
    """
    Represents a student's assessment submission
    """
    assessment = models.ForeignKey('Assessment', related_name='submissions')
    student = models.ForeignKey('Student')
    file = models.FileField(upload_to='submissions')
    remarks = models.TextField()
    mark = models.PositiveIntegerField()
    grade = models.CharField(max_length=2)

    def __str__(self):
        return "{} {}".format(self.assessment, self.student)
