from django.urls import path
from .views import Items,Saler, order_shipping, price_product,Edit,Delete,Login,Logout,AddUser,UserList,notify,side,Customer_List,Product_List,UpdateProduct,UpdateCustomer
urlpatterns = [
    path('product/', Items , name='product'),
    path('customer/', Saler , name='customer'),
    path('order/', order_shipping, name='order'),
    path('edit/<int:id>', Edit, name='edit'),
    path('delete/<int:id>/<str:action>/', Delete, name='delete'),
    path('prodcut-price/', price_product, name='pro'),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('adduser/', AddUser, name='add'),
    path('userlist/', UserList ,name='userlist'),
    path('notify/', notify ,name='notify'),
    path('side/', side ,name='side'),
    path('customerlist/', Customer_List ,name='customerlist'),
    path('productlist/', Product_List ,name='productlist'),
    path('updateproduct/<int:id>', UpdateProduct ,name='updateproduct'),
    path('updatecustomer/<int:id>', UpdateCustomer ,name='updatecustomer'),
]
