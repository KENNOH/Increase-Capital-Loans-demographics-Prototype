# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib import admin
from .models import Unit_station_names, Loan_status, Loans, Customers, Repayments


def roles(self):
    #short_name = unicode # function to get group name
    def short_name(x): return str(x)[:10].upper()  # first letter of a group
    p = sorted([u"<a title='%s'>%s</a>" % (x, short_name(x))
                for x in self.groups.all()])
    if self.user_permissions.count():
        p += ['+']
    value = ', '.join(p)
    return mark_safe("<nobr>%s</nobr>" % value)


roles.allow_tags = True
roles.short_description = u'Groups'


def last(self):
  fmt = "%Y %b %d, %H:%M"
  #fmt = "%Y %b %d, %H:%M:%S"
  if self.last_login is None:
    value = self.last_login
  else:
    value = self.last_login.strftime(fmt)

  return mark_safe("<nobr>%s</nobr>" % value)


last.allow_tags = True
last.admin_order_field = 'last_login'


def adm(self):
    return self.is_superuser


adm.boolean = True
adm.admin_order_field = 'is_superuser'


def staff(self):
    return self.is_staff


staff.boolean = True
staff.admin_order_field = 'is_staff'


def persons(self):
    return ', '.join(['<a href="%s">%s</a>' % (reverse('admin:auth_user_change', args=(x.id,)), x.username) for x in self.user_set.all().order_by('username')])


persons.allow_tags = True


class UserAdmin(UserAdmin):
    list_display = ['id', 'username', 'email', 'first_name',
                    'last_name', 'is_active', staff, adm, roles, last]
    list_filter = ['groups', 'id', 'is_staff', 'is_superuser', 'is_active']
    list_per_page = 50
    list_display_links = ['username']
    search_fields = ['username', 'email']


class GroupAdmin(GroupAdmin):
    list_display = ['name']
    list_display_links = ['name']
    list_per_page = 20


class EventModelAdmin(admin.ModelAdmin):
    list_display = ["name","phone","email","customer_id","created_at","loan_status","gender"]
    list_display_links = ["name"]
    list_filter = ["gender","loan_status"]
    list_per_page = 20
    list_editable = []
    search_fields = []

    class Meta:
        model = Customers


class EventModelAdmin2(admin.ModelAdmin):
    list_display = ["name", "phone", "loan_code",
                    "repayment_date", "amount_paid"]
    list_display_links = ["name"]
    list_filter = []
    list_per_page = 20
    list_editable = []
    search_fields = []

    class Meta:
        model = Repayments

admin.site.site_header = 'Increase Capital Loans Admin Panel'
admin.site.unregister(User)  # Unregister user to add new inline ProfileInline
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)  # Register User with this inline profile
admin.site.register(Group, GroupAdmin)
admin.site.register(Customers, EventModelAdmin)
admin.site.register(Repayments, EventModelAdmin2)
# Register your models here.
