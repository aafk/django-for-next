from django.db import models
from datetime import date as Date
from django.contrib.auth.models import User

# Create your models here.
class AccountLevel(models.Model):
    def __str__(self):
        if (self.parent.name == ''):
            return "%s"%(self.name)
        elif (self.parent.parent.name == ''):
            return "%s / %s"%(self.parent.name,self.name)
        else:
            return "%s / %s / %s"%(self.parent.parent.name,self.parent.name,self.name)
    def levels(self):
        if (self.parent.name == ''):
            return {
                'level1': self.id
            }
        elif (self.parent.parent.name == ''):
            return {
                'level1': self.parent.id,
                'level2': self.id,
            }
        else:
            return {
                'level1': self.parent.parent.id,
                'level2': self.parent.id,
                'level3': self.id,
            }
    class Meta:
        db_table="account_level"
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50, default='', blank=True)
    parent=models.ForeignKey('AccountLevel', on_delete=models.CASCADE, default=1)
    date_created=models.DateField(default=Date.today)

class Account(models.Model):
    def __str__(self):
        return "%s <%s>"%(self.name, self.levelID)
    # def save(self, user_id, *args, **kwargs):
    #     self.date_created = Date.today()
    #     self.user_created = User.objects.get(pk=user_id)
    #     self.full_clean()
    #     return super(Account, self).save(*args, **kwargs)
    class Meta:
        db_table="account"
        unique_together = ['levelID', 'code']
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50, default='')
    levelID=models.ForeignKey(AccountLevel, on_delete=models.CASCADE, default=1)
    code=models.CharField(max_length=50, default='')
    user_created=models.ForeignKey(User, on_delete=models.CASCADE)
    date_created=models.DateField(default=Date.today)

class DepreciationLevel(models.Model):
    def __str__(self):
        return self.name
    class Meta:
        db_table="depreciation_level"
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20, default='')
    date_created=models.DateField(default=Date.today)

class Depreciation(models.Model):
    def __str__(self):
        return self.name
    class Meta:
        db_table="depreciation"
    id=models.AutoField(primary_key=True)
    accountID=models.ForeignKey(Account, on_delete=models.CASCADE)
    levelID=models.ForeignKey(DepreciationLevel, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    depreciation=models.BooleanField()
    brand=models.CharField(max_length=50)
    type=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=15, decimal_places=3)
    purchase_month=models.DateField()
    detail=models.CharField(max_length=500)
    notes=models.CharField(max_length=500)
    user_created=models.ForeignKey(User, on_delete=models.CASCADE)
    date_created=models.DateField(default=Date.today)

class DepreciationProgress(models.Model):
    def __str__(self):
        return self.name
    class Meta:
        db_table="depreciation-progress"
    id=models.AutoField(primary_key=True)
    year=models.CharField(max_length=4, default='')
    depreciation=models.ForeignKey(Depreciation, on_delete=models.CASCADE)
    depreciation_amount=models.DecimalField(max_digits=15, decimal_places=0, default=0)

class DepreciationYear(models.Model):
    def __str__(self):
        return self.name
    class Meta:
        db_table="depreciation-year"
    id=models.AutoField(primary_key=True)
    level2ID=models.CharField(max_length=2, default='')
    name=models.CharField(max_length=20, default='')
    yearly_rate=models.DecimalField(max_digits=15, decimal_places=0, default=0)
    closed=models.BooleanField()

class Person(models.Model):
    class Meta:
        db_table="person"
    def __str__(self):
        return self.name
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    person_role=models.BooleanField(default=True)
    active=models.BooleanField(default=True)
    company= models.CharField(max_length=50)
    accupation= models.CharField(max_length=50)
    mobile1=models.CharField(max_length=20)
    mobile2=models.CharField(max_length=20, default='')
    address=models.CharField(max_length=50)
    date_created=models.DateField(default=Date.today)
    user_created=models.ForeignKey(User, on_delete=models.CASCADE)

class Measure(models.Model):
    class Meta:
        db_table="measure"
        ordering = ['date_created']
    def __str__(self):
        return self.name
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50, default='')
    date_created=models.DateField(default=Date.today)
    user_created=models.ForeignKey(User, on_delete=models.CASCADE)

class Inventory(models.Model):
    def __str__(self):
        return self.name
    class Meta:
        db_table="inventory"
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    type=models.CharField(max_length=50)
    accountID=models.ForeignKey(Account, on_delete=models.CASCADE)
    customerID=models.ForeignKey(Person, on_delete=models.CASCADE)
    measureID=models.ForeignKey(Measure, on_delete=models.CASCADE)
    avg_price=models.DecimalField(max_digits=15, decimal_places=3, default=0)
    detail=models.CharField(max_length=500)
    notes =models.CharField(max_length=500)
    date_created=models.DateField(default=Date.today)
    user_created=models.ForeignKey(User, on_delete=models.CASCADE)

class Document(models.Model):
    class Meta:
        db_table="document"
    id=models.AutoField(primary_key=True)
    date=models.DateField(default=Date.today)
    note=models.CharField(max_length=150,blank=True, default='')
    user_created=models.ForeignKey(User, on_delete=models.CASCADE)
    date_created=models.DateField(default=Date.today)

class Transaction(models.Model):
    class Meta:
        db_table="transaction"
    id=models.AutoField(primary_key=True)
    docID=models.ForeignKey(Document, on_delete=models.PROTECT, null=True)
    accountID=models.ForeignKey(Account, on_delete=models.CASCADE)
    customerID=models.ForeignKey(Person, on_delete=models.CASCADE)
    date=models.DateField(default=Date.today)
    credit=models.DecimalField(max_digits=15, decimal_places=0)
    debit=models.DecimalField(max_digits=15, decimal_places=0)
    note =models.CharField(max_length=50, default='')
    date_created=models.DateField(default=Date.today)
    user_created=models.ForeignKey(User, on_delete=models.CASCADE)

class InventoryTransaction(models.Model):
    def __str__(self):
        return self.name
    class Meta:
        db_table="inventory-transaction"
    id=models.AutoField(primary_key=True)
    docID=models.ForeignKey(Document, on_delete=models.PROTECT, null=True)
    inventoryID=models.ForeignKey(Inventory, on_delete=models.PROTECT, null=True)
    customerID=models.ForeignKey(Person, on_delete=models.PROTECT, null=True)

