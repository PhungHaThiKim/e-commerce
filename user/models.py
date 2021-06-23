from django.db import models


class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    birthday = models.CharField(db_column='Birthday', max_length=255)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=255, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    phone = models.CharField(db_column='Phone', max_length=255, blank=True, null=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'user'


class Address(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID', blank=True,
                               null=True)  # Field name made lowercase.
    homenum = models.CharField(db_column='HomeNum', max_length=255, blank=True, null=True)  # Field name made lowercase.
    street = models.CharField(db_column='Street', max_length=255, blank=True, null=True)  # Field name made lowercase.
    district = models.CharField(db_column='District', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=255, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'address'


class Fullname(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('User', models.DO_NOTHING, db_column='UserID', blank=True,
                               null=True)  # Field name made lowercase.
    first = models.CharField(db_column='First', max_length=255, blank=True, null=True)  # Field name made lowercase.
    last = models.CharField(db_column='Last', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'fullname'

class Employee(models.Model):
    position = models.CharField(db_column='Position', max_length=255)  # Field name made lowercase.
    salary = models.FloatField(db_column='Salary', blank=True, null=True)  # Field name made lowercase.
    exp = models.IntegerField(db_column='Exp', blank=True, null=True)  # Field name made lowercase.
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'employee'

class Customer(models.Model):
    type = models.CharField(db_column='Type', max_length=255)  # Field name made lowercase.
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.

    class Meta:
        db_table = 'customer'

class Logsearch(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customeruserid = models.ForeignKey('Customer', models.DO_NOTHING, db_column='CustomerUserID')  # Field name made lowercase.
    time = models.DateField(db_column='Time')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255)  # Field name made lowercase.

    class Meta:
        db_table = 'logsearch'


class Logviewdetail(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customeruserid = models.ForeignKey('Customer', models.DO_NOTHING, db_column='CustomerUserID')  # Field name made lowercase.
    time = models.DateField(db_column='Time')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255)  # Field name made lowercase.

    class Meta:
        db_table = 'logviewdetail'

