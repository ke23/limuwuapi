from django.shortcuts import render

from django.views.generic import ListView
from membership.models import Membership, UserMembership, Subscription


class MembershipView(ListView):

    model = Membership
    template_name = 'membership/list.html'


    # def get_user_membership(self):
    #     # print(self.request.user)
    #     user_membership_qs = UserMembership.objects.filter(user=self.request.user.id)
    #     if user_membership_qs.exists():
    #         return user_membership_qs.first()
    #     return None
    

    def get_context_data(self, *args, **kwargs):
        print(self.request.META)
        context = super().get_context_data(**kwargs)
        # print("ini context")
        print(context)
        # current_membership = self.get_user_membership()
        # context['current_membership'] = str(current_membership.membership)
        return context