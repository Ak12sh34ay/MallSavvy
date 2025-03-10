import datetime
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from mall_savvy_app.models import *


def logins(request):
    return render(request,"login_index.html")

def login_post(request):
    un = request.POST['name']
    pwd = request.POST['pass']

    res = login.objects.filter(username=un,password=pwd)
    if res.exists():
        res=res[0]
        if res.usertype == 'admin':
            request.session['lid'] = res.id
            return HttpResponse('<script>alert("login successful");window.location="/adminhome"</script>')
        elif res.usertype == 'shop':
            request.session['lid'] = res.id
            request.session['sid'] = shop.objects.get(LOGIN=res.id).id
            return HttpResponse('<script>alert("login successful");window.location="/shophome"</script>')
        elif res.usertype == 'customer':
            request.session['lid'] = res.id
            request.session['cid'] = customer.objects.get(LOGIN=res.id).id
            return HttpResponse('<script>alert("login successful");window.location="/customerhome"</script>')
        elif res.usertype == 'security':
            request.session['lid'] = res.id
            request.session['secid'] = security.objects.get(LOGIN=res.id).id
            return HttpResponse('<script>alert("login successful");window.location="/securityhome"</script>')
        else:
            return HttpResponse('<script>alert("login failed");window.location="/logins"</script>')
    else:
        return HttpResponse('<script>alert("failed");window.location="/logins"</script>')

def main_index(request):

    return render(request,"index.html")

def logout(request):
    del request.session['lid']
    return HttpResponse('<script>alert("logout");window.location="/logins"</script>')


#admin

def adminhome(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = ""
    return render(request,"admin/index.html")

def view_shop(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW SHOP"
    data = shop.objects.filter(LOGIN__usertype='pending')
    return render(request,"admin/View and Verify shop.html",{"data":data})

def approve_shop(request,id):
    login.objects.filter(id=id).update(usertype='shop')
    return HttpResponse('<script>alert("approved");window.location="/view_shop#aa"</script>')

def reject_shop(request,id):
    login.objects.filter(id=id).update(usertype='rejected')
    return HttpResponse('<script>alert("rejected");window.location="/view_shop#aa"</script>')

def view_approved_shop(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW APPROVED SHOP"
    data = shop.objects.filter(LOGIN__usertype='shop')
    return render(request,"admin/view verified shop.html",{"data":data})

def add_parking_slot(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "ADD PARKING SLOT"
    return render(request,"admin/add_parking_slot.html")

def add_parking_slot_post(request):
    no = request.POST['textfield']
    type = request.POST['select']

    obj = slot()
    obj.slot_no=no
    obj.vehicle_type=type
    obj.status='available'
    obj.save()

    return HttpResponse('<script>alert("Added");window.location="/view_parking_slot#aa"</script>')

def view_parking_slot(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW PARKING SLOT"
    data=slot.objects.all()
    return render(request,"admin/view_parking_slot.html",{"data":data})

def delete_parking_slot(request,id):
    slot.objects.filter(id=id).delete()
    return HttpResponse('<script>alert("deleted");window.location="/view_parking_slot#aa"</script>')

def view_slot_booking(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW SLOT BOOKING"
    data=booking.objects.all()
    return render(request,"admin/view_bookings.html",{"data":data})

def add_rental_space(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "ADD RENTAL SPACE"
    return render(request,"admin/add_rental_space.html")

def add_rental_space_post(request):
    flr = request.POST['textfield']
    des = request.POST['textarea']
    amt = request.POST['textfield3']

    img = request.FILES['fileField']
    d=datetime.datetime.now().strftime('%d%m%y-%H%M%S')
    fs=FileSystemStorage()
    fs.save(r'C:\Users\DELL\PycharmProjects\Mall_Savvy\mall_savvy_app\static\images\\'+ d +'.jpg', img)
    path='/static/images/'+ d + '.jpg'

    obj=rentspace()
    obj.floor=flr
    obj.description=des
    obj.amount=amt
    obj.image=path
    obj.status='pending'
    obj.save()
    return HttpResponse('<script>alert("added");window.location="/view_rental_space#aa"</script>')

def view_rental_space(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW RENTAL SPACE"
    data=rentspace.objects.all()
    return render(request,"admin/view_rental_space.html",{"data":data})

def update_rental_space(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "UPDATE RENTAL SPACE"
    data=rentspace.objects.get(id=id)
    return render(request,"admin/update_rental_space.html",{"data":data})

def update_rental_space_post(request,id):
    flr = request.POST['textfield']
    des = request.POST['textarea']
    amt = request.POST['textfield3']

    if 'fileField' in request.FILES:
        img = request.FILES['fileField']
        d=datetime.datetime.now().strftime('%d%m%y-%H%M%S')
        fs=FileSystemStorage()
        fs.save(r'C:\Users\DELL\PycharmProjects\Mall_Savvy\mall_savvy_app\static\images\\'+ d +'.jpg', img)
        path='/static/images/'+ d + '.jpg'
        rentspace.objects.filter(id=id).update(floor=flr,description=des,amount=amt,image=path)
        return HttpResponse('<script>alert("updated");window.location="/view_rental_space#aa"</script>')
    else:
        rentspace.objects.filter(id=id).update(floor=flr,description=des,amount=amt)
        return HttpResponse('<script>alert("updated");window.location="/view_rental_space#aa"</script>')



def delete_rental_space(request,id):
    rentspace.objects.filter(id=id).delete()
    return HttpResponse('<script>alert("deleted");window.location="/view_rental_space#aa"</script>')

def view_rental_request_shop(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW RENTAL REQUEST FORM SHOP"
    data=rentrequest_shop.objects.filter(RENTSPACE_id=id,rent_request_status='pending')
    return render(request,"admin/view_request_from_shop.html",{"data":data})

def approve_rental_request_shop(request,id):
    rentrequest_shop.objects.filter(id=id).update(rent_request_status='approved')
    return HttpResponse('<script>alert("approved");window.location="/view_rental_space#aa"</script>')

def reject_rental_request_shop(request,id):
    rentrequest_shop.objects.filter(id=id).update(rent_request_status='rejected')
    return HttpResponse('<script>alert("rejected");window.location="/view_rental_space#aa"</script>')
#
# def view_approved_rental_request_shop(request):
#     data = rentrequest_shop.objects.filter(rent_request_status='approved')
#     return render(request,"admin/")

def view_rental_request_customer(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW RENTAL REQUEST FROM CUSTOMER"
    data = rentrequest_customer.objects.filter(RENTSPACE_id=id,rent_request_status='pending')
    return render(request,"admin/view_request_from_user.html",{"data":data})

def approve_rental_request_customer(request,id):
    rentrequest_customer.objects.filter(id=id).update(rent_request_status='approved')
    return HttpResponse('<script>alert("approved");window.location="/view_rental_request_customer#aa"</script>')

def reject_rental_request_customer(request,id):
    rentrequest_customer.objects.filter(id=id).update(rent_request_status='rejected')
    return HttpResponse('<script>alert("rejected");window.location="/view_rental_request_customer#aa"</script>')
#
# def view_approved_rental_request_customer(request):
#     data = rentrequest_customer.objects.filter(rent_request_status='approved')
#     return render(request,"admin/")
#
def view_payment(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW PAYMENT"
    data=booking.objects.filter(status='paid')
    return render(request,"admin/view_payment.html",{"data":data})

def add_security(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "ADD SECURITY"
    return render(request,"admin/add_security.html")

def add_security_post(request):
    nm = request.POST['textfield']
    eml = request.POST['textfield2']
    phn = request.POST['textfield3']
    pwd=random.randint(0000,9999)

    res=security.objects.filter(email=eml,phone=phn)
    if res.exists():
        return HttpResponse('<script>alert("already exista=s");window.location="/add_security"</script>')
    else:
        obj = login()
        obj.username=eml
        obj.password=pwd
        obj.usertype='security'
        obj.save()

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("mallsavvyakshay@gmail.com", "wnsb nyoo htau npeb")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "mallsavvyakshay@gmail.com"
        msg['To'] = eml
        msg['Subject'] = "registration request"
        body = "your registration request approved sucessfully.." + str(pwd)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)

        obj1 = security()
        obj1.name=nm
        obj1.email=eml
        obj1.phone=phn
        obj1.LOGIN=obj
        obj1.save()
        return HttpResponse('<script>alert("added");window.location="/view_security#aa"</script>')

def view_security(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW SECURITY"
    data=security.objects.all()
    return render(request,"admin/view security.html",{"data":data})

def update_security(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "UPDATE SECURITY"
    data=security.objects.get(id=id)
    return render(request,"admin/update_security.html",{"data":data})

def update_security_post(request,id):
    nm = request.POST['textfield']
    eml = request.POST['textfield2']
    phn = request.POST['textfield3']
    security.objects.filter(id=id).update(name=nm,email=eml,phone=phn)
    return HttpResponse('<script>alert("updated");window.location="/view_security#aa"</script>')

def delete_security(request,id):
    security.objects.filter(id=id).delete()
    return HttpResponse('<script>alert("deleted");window.location="/view_security#aa"</script>')

#################################################################


#  shop

def register(request):
    return render(request,'shop/register_index.html')

def register_post(request):
    nm = request.POST['name']
    eml = request.POST['email']
    phn = request.POST['phone']
    bio = request.POST['bio']

    prf = request.FILES['fileField']
    d=datetime.datetime.now().strftime("%d%m%y-%H%M%S")
    fs=FileSystemStorage()
    fs.save(r"C:\Users\DELL\PycharmProjects\Mall_Savvy\mall_savvy_app\static\images\\"+ d+ '.pdf',prf)
    path='static/images/'+ d+ '.pdf'

    pwd = request.POST['password']
    cpwd = request.POST['cpassword']

    res = login.objects.filter(username=eml)
    if res.exists():
        return HttpResponse('<script>alert("email already registered");window.location="/register"</script>')
    elif pwd == cpwd:
        obj = login()
        obj.username=eml
        obj.password=pwd
        obj.usertype='pending'
        obj.save()

        ob = shop()
        ob.name=nm
        ob.email=eml
        ob.phone=phn
        ob.bio=bio
        ob.proof=path
        ob.LOGIN=obj
        ob.save()
        return HttpResponse('<script>alert("Registered");window.location="/logins"</script>')
    else:
        return HttpResponse('<script>alert("password does not match");window.location="/register"</script>')

def shophome(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = ""
    return render(request,'shop/index.html')

def add_product(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "ADD PRODUCT"
    return render(request,"shop/add_product.html")

def add_product_post(request):
    nm = request.POST['textfield']
    prc = request.POST['textfield3']
    img = request.FILES['textfield2']

    d = datetime.datetime.now().strftime('%d%m%y-%H%M%S')
    fs = FileSystemStorage()
    fs.save(r'C:\Users\DELL\PycharmProjects\Mall_Savvy\mall_savvy_app\static\images\\' + d + '.jpg', img)
    path = '/static/images/' + d + '.jpg'

    obj = product()
    obj.name=nm
    obj.price=prc
    obj.image=path
    obj.SHOP_id=request.session['sid']
    print(request.session['sid'])
    obj.save()
    return HttpResponse('<script>alert("added");window.location="/view_product#aa"</script>')

def view_product(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW PRODUCT"
    data=product.objects.filter(SHOP=request.session['sid'])
    print(data,"llllllllllllllllllll")
    print(request.session['sid'])
    return render(request,"shop/shop_product_view.html",{"data":data})

def update_product(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "UPDATE PRODUCT"
    data=product.objects.get(id=id)
    return render(request,"shop/update_product.html",{"data":data})

def update_product_post(request,id):
    # nm = request.POST['textfield']
    # prc = request.POST['textfield3']

    try:
        nm = request.POST['textfield']
        prc = request.POST['textfield3']
        img = request.FILES['fileField']
        d = datetime.datetime.now().strftime('%d%m%y-%H%M%S')
        fs = FileSystemStorage()
        fs.save(r'C:\Users\DELL\PycharmProjects\Mall_Savvy\mall_savvy_app\static\images\\' + d + '.jpg', img)
        path = '/static/images/' + d + '.jpg'
        product.objects.filter(id=id).update(name=nm, price=prc, image=path)
        return HttpResponse('<script>alert("updated");window.location="/view_product#aa"</script>')
    except Exception as e:
        nm = request.POST['textfield']
        prc = request.POST['textfield3']
        product.objects.filter(id=id).update(name=nm, price=prc,)
        return HttpResponse('<script>alert("updated");window.location="/view_product#aa"</script>')

    # if 'fileField' in request.FILES:
    #     img = request.FILES['fileField']
    #     d=datetime.datetime.now().strftime('%d%m%y-%H%M%S')
    #     fs=FileSystemStorage()
    #     fs.save(r'C:\Users\kiran\PycharmProjects\Mall_Savvy\mall_savvy_app\static\images\\'+ d +'.jpg', img)
    #     path='/static/images/'+ d + '.jpg'
    #     product.objects.filter(id=id).update(name=nm,price=prc,image=path)
    #     return HttpResponse('<script>alert("updated");window.location="/view_product"</script>')
    # else:
    #     product.objects.filter(id=id).update(name=nm,price=prc,)
    #     return HttpResponse('<script>alert("updated");window.location="/view_product"</script>')


def delete_product(request,id):
    product.objects.filter(id=id).delete()
    return HttpResponse('<script>alert("deleted");window.location="/view_product#aa"</script>')

def add_product_offer(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "ADD PRODUCT OFFER"
    request.session['pid']=id
    return render(request,"shop/product_offer_add.html",{"id":id})

def add_product_offer_post(request,id):
    pid=request.session['pid']
    dis = request.POST['textfield3']
    frm = request.POST['textfield']
    to = request.POST['textfield2']

    obj = product_offer()
    obj.discount=dis
    obj.from_date=frm
    obj.to_date=to
    obj.PRODUCT_id=id
    obj.save()
    return HttpResponse('<script>alert("added");window.location="/view_product_offer/'+str(pid)+'#aa"</script>')

def view_product_offer(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW PRODUCT OFFER"
    request.session['pid'] = id
    data=product_offer.objects.filter(PRODUCT_id=id)
    return render(request,"shop/product_offer_view.html",{"data":data})

def update_product_offer(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "UPDATE PRODUCT OFFER"
    data=product_offer.objects.get(id=id)
    return render(request,"shop/product_offer_update.html",{"data":data})

def update_product_offer_post(request,id):
    pid=request.session['pid']
    dis = request.POST['textfield3']
    frm = request.POST['textfield']
    to = request.POST['textfield2']
    product_offer.objects.filter(id=id).update(discount=dis,from_date=frm,to_date=to)
    return HttpResponse('<script>alert("updated");window.location="/view_product_offer/'+str(pid)+'#aa"</script>')

def delete_product_offer(request,id):
    pid = request.session['pid']
    product_offer.objects.filter(id=id).delete()
    return HttpResponse('<script>alert("deleted");window.location="/view_product_offer/'+str(pid)+'#aa"</script>')

def view_todays_bill(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW TODAYS BILL"
    d=datetime.datetime.now().strftime('%d-%m-%Y')
    data=bill_sub.objects.filter(BILL__date = d)
    return render(request,"shop/view_todays_bill.html",{"data":data})

def view_previous_bill(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW PREVIOUS BILL"
    d=datetime.datetime.now().strftime('%d-%m-%Y')
    data=bill_sub.objects.filter(BILL__date__lt = d)
    return render(request,"shop/view_previous_bill.html",{"data":data})

def view_rent_space_shp(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW RENT SPACE"

    data=rentspace.objects.all()
    return render(request,"shop/view_rent_space.html",{"data":data})

def sent_rent_request_shp(request,id):
    obj= rentrequest_shop()
    obj.RENTSPACE_id=id
    obj.rent_request_status='pending'
    obj.date=datetime.datetime.now()
    obj.SHOP_id=request.session['sid']
    obj.save()
    return HttpResponse('<script>alert("request sent");window.location="/view_rent_request_status_shp#aa"</script>')

def view_rent_request_status_shp(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW RENT SPACE STATUS"
    data=rentrequest_shop.objects.filter(SHOP=request.session['sid'])
    return render(request,"shop/view_request_status.html",{"data":data})



##################################################


#          customer


def register_customer(request):
    return render(request,"customer/register_index.html")

def register_cusomer_post(request):
    nm = request.POST['name']
    eml = request.POST['email']
    phn = request.POST['phone']
    plc = request.POST['place']
    pwd = request.POST['password']
    cpwd = request.POST['cpassword']

    res = login.objects.filter(username=eml)
    if res.exists():
        return HttpResponse('<script>alert("email already registered");window.location="/register"</script>')
    elif pwd == cpwd:
        obj = login()
        obj.username=eml
        obj.password=pwd
        obj.usertype='customer'
        obj.save()

        ob = customer()
        ob.name=nm
        ob.email=eml
        ob.phone=phn
        ob.place=plc
        ob.LOGIN=obj
        ob.save()
        return HttpResponse('<script>alert("Registered");window.location="/"</script>')
    else:
        return HttpResponse('<script>alert("password does not match");window.location="/register"</script>')

def customerhome(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = ""
    return render(request,"customer/index.html")

def view_shop_cust(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW SHOP"
    data=shop.objects.all()
    return render(request,"customer/view_shop.html",{"data":data})

def view_product_cust(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW PRODUCT"
    request.session['pid']=id
    data=product_offer.objects.filter(id=id)
    return render(request,"customer/view_product.html",{"data":data})

def like_offer(request,id):
    pid=request.session['pid']
    obj=likes()
    obj.PRODUCTOFFER_id=id
    obj.CUSTOMER_id=request.session['cid']
    obj.save()
    return HttpResponse('<script>alert("liked");window.location="/view_product_cust/'+str(pid)+'#aa"</script>')

def view_liked_offer(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW LIKED OFFER"
    data = likes.objects.filter(CUSTOMER=request.session['cid'])
    return render(request,"customer/view_liked_product.html",{"data":data})

def add_to_cart(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "ADD TO CART"
    return render(request,"customer/add_to_cart.html",{"id":id})

def addto_cart_post(request,id):
    quantity = request.POST['Quantity']
    res=cart.objects.filter(CUSTOMER=request.session['cid'],PRODUCTOFFER_id=id)
    if res.exists():
        qn=res[0].quantity
        tot=int(qn)+int(quantity)
        cart.objects.filter(PRODUCTOFFER_id=id).update(quantity=tot)
        return HttpResponse('<script>alert("cart updated");window.location="/customerhome"</script>')
    else:
        obj=cart()
        obj.quantity=quantity
        obj.PRODUCTOFFER_id=id
        obj.CUSTOMER_id=request.session['cid']
        obj.save()
        return HttpResponse('<script>alert("product added to cart");window.location="/customerhome"</script>')

def view_cart(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "CART"
    data = cart.objects.filter(CUSTOMER_id=request.session['cid'])
    tot=0
    for i in data:
        total=int(i.PRODUCTOFFER.discount)*int(i.quantity)
        tot=int(tot)+int(total)

    return render(request, "customer/view_cart.html",{"data":data,"total":tot})

def remove_cart(request,id):
    cart.objects.filter(id=id).delete()
    return HttpResponse('<script>alert("artwork removed");window.location="/view_cart"</script>')

def place_order(request):
    res = cart.objects.filter(CUSTOMER_id=request.session['cid'])
    if res.exists():
        shop=[]
        for i in res:
            if i.PRODUCTOFFER.PRODUCT.SHOP_id  not in shop:
                shop.append(i.PRODUCTOFFER.PRODUCT.SHOP_id)
            else:
                pass
        for j in shop:
            obj = bill()
            obj.amount = 0
            obj.SHOP_id = j
            obj.CUSTOMER_id = request.session['cid']
            obj.date = datetime.datetime.now().strftime("%d-%m-%Y")
            obj.save()
            re=cart.objects.filter(PRODUCTOFFER__PRODUCT__SHOP_id =j)
            tot = 0
            for k in re:
                amnt = int(k.quantity) * int(k.PRODUCTOFFER.discount)
                tot = int(tot) + int(amnt)
                ob1 = bill_sub()
                ob1.BILL = obj
                ob1.PRODUCTOFFER = k.PRODUCTOFFER
                ob1.quantity = k.quantity
                ob1.save()
                k.delete()
            bill.objects.filter(id=obj.id).update(amount=tot)
        return HttpResponse('<script>alert("order placed");window.location="/customerhome"</script>')
    else:
        return HttpResponse('<script>alert("cart is empty");window.location="/view_cart"</script>')

def view_bill_cust(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW BILL"
    data=bill_sub.objects.filter(BILL__CUSTOMER=request.session['cid'])
    return render(request,"customer/view_bill.html",{"data":data})

def view_rent_space(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW RENTSPACE"
    data=rentspace.objects.all()
    return render(request,"customer/view_rent_space.html",{"data":data})

def sent_rent_request(request,id):
    obj= rentrequest_customer()
    obj.RENTSPACE_id=id
    obj.rent_request_status='pending'
    obj.date=datetime.datetime.now()
    obj.CUSTOMER_id=request.session['cid']
    obj.save()
    return HttpResponse('<script>alert("request sent");window.location="/view_rent_request_status#aa"</script>')

def view_rent_request_status(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW RENT REQUEST STATUS"
    data=rentrequest_customer.objects.filter(CUSTOMER_id=request.session['cid'])
    return render(request,"customer/view_request_status.html",{"data":data})

def view_slot(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW SLOT"

    data=slot.objects.filter(status='available')
    return render(request,"customer/view_parking_slot.html",{"data":data})

def book_slot(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "BOOK SLOT"
    return render(request,"customer/book_slot.html",{"id":id})

def book_slot_post(request,id):
    d = request.POST['textfield']
    frm = request.POST['textfield2']
    to = request.POST['textfield3']

    obj = booking()
    obj.date=d
    obj.SLOT_id=id
    obj.from_time=frm
    obj.to_time=to
    obj.check_in_time='pending'
    obj.check_out_time='pending'
    obj.amount='pending'
    obj.status='pending'
    obj.CUSTOMER_id=request.session['cid']
    obj.save()
    return HttpResponse('<script>alert("booked");window.location="/view_slot#aa"</script>')

##########################


#       security

def securityhome(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = ""
    return render(request,"security/index.html")

def view_parking_booking(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW BOOKING"
    data=booking.objects.filter(status='pending')
    return render(request,"security/view_booking.html",{"data":data})

def approve_parking_booking(request,id):
    booking.objects.filter(id=id).update(status='approved')
    rs=booking.objects.filter(id=id)
    if rs.exists():
        sl=rs[0].SLOT_id
        slot.objects.filter(id=sl).update(status='booked')
    else:
        pass
    return HttpResponse('<script>alert("approved");window.location="/view_parking_booking#aa"</script>')

def reject_parking_booking(request,id):
    booking.objects.filter(id=id).update(status='rejected')

    return HttpResponse('<script>alert("rejected");window.location="/view_parking_booking#aa"</script>')

def view_approved_parking_booking(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "VIEW APPROVED BOOKING"
    data = booking.objects.filter(status='approved')
    return render(request,"security/view_approved_booking.html",{"data":data})

def view_slot_sec(request):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    data=slot.objects.all()
    return render(request,"security/view_slot.html",{"data":data})

def update_parking_status(request,id):
    slot.objects.filter(id=id).update(status='available')
    return HttpResponse('<script>alert("updated");window.location="/view_slot_sec#aa"</script>')

def payment_entry(request,id):
    if "lid" not in request.session:
        return HttpResponse('<script>alert("Session Expired...please login again");window.location="/"</script>')
    request.session['head'] = "PAYMENT ENTRY"
    return render(request,"security/payment_entry.html",{"id":id})

def payment_entry_post(request,id):
    checkin = request.POST['textfield']
    checkout = request.POST['textfield2']
    amt = request.POST['textfield3']
    booking.objects.filter(id=id).update(check_in_time=checkin,check_out_time=checkout,amount=amt,status='paid')
    return HttpResponse('<script>alert("updated");window.location="/view_approved_parking_booking#aa"</script>')
