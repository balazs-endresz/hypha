from django.shortcuts import render
from django.views.generic import TemplateView
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableView

from opentech.apply.funds.models import ApplicationSubmission, RoundsAndLabs
from opentech.apply.funds.tables import AdminSubmissionsTable, SubmissionsTable, SummarySubmissionsTable
from opentech.apply.utils.views import ViewDispatcher


class AdminDashboardView(TemplateView):

    def get(self, request, *args, **kwargs):
        qs = ApplicationSubmission.objects.all().for_table(self.request.user)

        in_review = SubmissionsTable(qs.in_review_for(request.user), prefix='in-review-')
        RequestConfig(request, paginate={'per_page': 10}).configure(in_review)
        base_query = RoundsAndLabs.objects.with_progress().active().order_by('-end_date')
        base_query = base_query.by_lead(request.user)
        open_rounds = base_query.open()[:6]
        open_query = '?round_state=open'
        closed_rounds = base_query.closed()[:6]
        closed_query = '?round_state=closed'
        rounds_title = 'Your rounds and labs'

        my_review_qs = qs.in_review_for(request.user).order_by('-submit_time')
        my_review = SummarySubmissionsTable(my_review_qs[:5], prefix='my-review-')
        display_more = (my_review_qs.count() > 5)

        return render(request, 'dashboard/dashboard.html', {
            'in_review': in_review,
            'open_rounds': open_rounds,
            'open_query': open_query,
            'closed_rounds': closed_rounds,
            'closed_query': closed_query,
            'rounds_title': rounds_title,
            'my_review': my_review,
            'in_review_count': my_review_qs.count(),
            'display_more': display_more,
        })


class ReviewerDashboardView(TemplateView):
    def get(self, request, *args, **kwargs):
        qs = ApplicationSubmission.objects.all().for_table(self.request.user)

        my_review_qs = qs.in_review_for(request.user).order_by('-submit_time')
        my_review = SummarySubmissionsTable(my_review_qs[:5], prefix='my-review-')
        display_more = (my_review_qs.count() > 5)

        also_in_review = AdminSubmissionsTable(
            qs.in_review_for(request.user, assigned=False).exclude(id__in=my_review_qs),
            prefix='also-in-review-'
        )
        RequestConfig(request, paginate={'per_page': 10}).configure(also_in_review)

        return render(request, 'dashboard/reviewer_dashboard.html', {
            'my_review': my_review,
            'in_review_count': my_review_qs.count(),
            'display_more': display_more,
            'also_in_review': also_in_review,
        })


class ApplicantDashboardView(SingleTableView):
    template_name = 'dashboard/applicant_dashboard.html'
    model = ApplicationSubmission
    table_class = SubmissionsTable

    def get_queryset(self):
        return self.model.objects.filter(
            user=self.request.user
        ).inactive().current().for_table(self.request.user)

    def get_context_data(self, **kwargs):
        my_active_submissions = self.model.objects.filter(
            user=self.request.user
        ).active().current().select_related('draft_revision')

        my_active_submissions = [
            submission.from_draft() for submission in my_active_submissions
        ]

        return super().get_context_data(
            my_active_submissions=my_active_submissions,
            **kwargs,
        )


class DashboardView(ViewDispatcher):
    admin_view = AdminDashboardView
    reviewer_view = ReviewerDashboardView
    applicant_view = ApplicantDashboardView
