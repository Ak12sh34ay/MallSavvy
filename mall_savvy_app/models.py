from django.db import models

# Create your models here.

class login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=100)


class shop(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    bio = models.CharField(max_length=100)
    proof = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(login,default=1,on_delete=models.CASCADE)


class security(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(login,default=1,on_delete=models.CASCADE)

class customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    LOGIN = models.ForeignKey(login,default=1,on_delete=models.CASCADE)

class slot(models.Model):
    slot_no = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

class product(models.Model):
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    SHOP = models.ForeignKey(shop,default=1,on_delete=models.CASCADE)


class product_offer(models.Model):
    discount = models.CharField(max_length=100)
    from_date = models.CharField(max_length=100)
    to_date = models.CharField(max_length=100)
    PRODUCT = models.ForeignKey(product,default=1,on_delete=models.CASCADE)

class likes(models.Model):
    PRODUCTOFFER = models.ForeignKey(product_offer,default=1,on_delete=models.CASCADE)
    CUSTOMER = models.ForeignKey(customer,default=1,on_delete=models.CASCADE)

class booking(models.Model):
    SLOT = models.ForeignKey(slot,default=1,on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    from_time = models.CharField(max_length=100)
    to_time = models.CharField(max_length=100)
    check_in_time = models.CharField(max_length=100)
    check_out_time = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    CUSTOMER = models.ForeignKey(customer,default=1,on_delete=models.CASCADE)

class rentspace(models.Model):
    floor = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    image = models.CharField(max_length=100)

class rentrequest_shop(models.Model):
    RENTSPACE = models.ForeignKey(rentspace,default=1,on_delete=models.CASCADE)
    rent_request_status = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    SHOP = models.ForeignKey(shop,default=1,on_delete=models.CASCADE)

class rentrequest_customer(models.Model):
    RENTSPACE = models.ForeignKey(rentspace,default=1,on_delete=models.CASCADE)
    rent_request_status = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    CUSTOMER = models.ForeignKey(customer,default=1,on_delete=models.CASCADE)

class bill(models.Model):
    amount = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    CUSTOMER = models.ForeignKey(customer,default=1,on_delete=models.CASCADE)
    SHOP = models.ForeignKey(shop,default=1,on_delete=models.CASCADE)

class bill_sub(models.Model):
    PRODUCT_OFFER = models.ForeignKey(product_offer,default=1,on_delete=models.CASCADE)
    BILL = models.ForeignKey(bill,default=1,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)

class cart(models.Model):
    PRODUCTOFFER = models.ForeignKey(product_offer,default=1,on_delete=models.CASCADE)
    CUSTOMER = models.ForeignKey(customer,default=1,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)
