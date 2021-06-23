from django.db import models
from user.models import User, Customer
from cart.models import CartItem

# Create your models here.
class Feedback(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    customeruserid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='CustomerUserID')  # Field name made lowercase.
    cartitemid = models.ForeignKey(CartItem, models.DO_NOTHING, db_column='CartItemID')  # Field name made lowercase.
    content = models.CharField(db_column='Content', max_length=255, blank=True, null=True)  # Field name made lowercase.
    star = models.IntegerField(db_column='Star', blank=True, null=True)  # Field name made lowercase.
    time = models.DateField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'feedback'