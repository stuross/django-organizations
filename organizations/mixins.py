from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from organizations.models import Organization, OrganizationUser


class OrganizationMixin(object):
    """Mixin used like a SingleObjectMixin to fetch an organization"""

    org_model = Organization
    org_context_name = 'organization'
    org_slug_url_kwarg = 'organization_slug'
    org_pk_url_kwarg = 'organization_pk'

    def get_org_model(self):
        return self.org_model

    def get_context_data(self, **kwargs):
        kwargs.update({self.org_context_name: self.get_organization()})
        return super(OrganizationMixin, self).get_context_data(**kwargs)

    def get_organization(self):
        if hasattr(self, 'organization'):
            return self.organization

        organization_pk = self.kwargs.get(self.org_pk_url_kwarg, None)
        organization_slug = self.kwargs.get(self.org_slug_url_kwarg, None)

        if organization_pk:
            self.organization = get_object_or_404(self.get_org_model().objects.select_subclasses(), pk=organization_pk, is_active=True)
        elif organization_slug is not None:
            self.organization = get_object_or_404(self.get_org_model().objects.select_subclasses(), slug=organization_slug, is_active=True)
        return self.organization
    #get_organization = get_object # Now available when `get_object` is overridden


class OrganizationUserMixin(OrganizationMixin):
    """Mixin used like a SingleObjectMixin to fetch an organization user"""

    user_model = OrganizationUser
    org_user_context_name = 'organization_user'

    def get_user_model(self):
        return self.user_model

    def get_context_data(self, **kwargs):
        kwargs = super(OrganizationUserMixin, self).get_context_data(**kwargs)
        kwargs.update({self.org_user_context_name: self.object,
            self.org_context_name: self.object.organization})
        return kwargs

    def get_object(self):
        """ Returns the OrganizationUser object based on the primary keys for both
        the organization and the organization user.
        """
        if hasattr(self, 'organization_user'):
            return self.organization_user
        organization = self.get_organization()
        user_pk = self.kwargs.get('user_pk', None)
        self.organization_user = get_object_or_404(
                OrganizationUser.objects.select_related(),
                user__pk=user_pk, organization=organization)
        return self.organization_user


class MembershipRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.organization = self.get_organization()
        if not self.organization.is_member(request.user) and not \
                    request.user.is_superuser:
            return HttpResponseForbidden(_("Wrong organization"))
        return super(MembershipRequiredMixin, self).dispatch(request, *args,
                **kwargs)


class AdminRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.organization = self.get_organization()
        if not self.organization.is_admin(request.user) and not \
                    request.user.is_superuser:
            return HttpResponseForbidden(_("Sorry, admins only"))
        return super(AdminRequiredMixin, self).dispatch(request, *args,
                **kwargs)


class OwnerRequiredMixin(object):
    """This mixin presumes that authentication has already been checked"""

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.organization = self.get_organization()
        if self.organization.owner.organization_user.user != request.user \
                    and not request.user.is_superuser:
            return HttpResponseForbidden(_("You are not the organization owner"))
        return super(OwnerRequiredMixin, self).dispatch(request, *args,
                **kwargs)
