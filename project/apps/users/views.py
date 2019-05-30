from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from project.apps.tables.models import Table
from project.apps.users.forms import SignupForm, LoginForm
from project.core.mixins import RequestFormMixin


class ProfileView(View):
    def get(self, request):
        tables = Table.objects.filter(user=request.user)
        context = {
            'tables': tables,
        }
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from datetime import date
        import random

        today = date.today().strftime("%d/%m/%Y")

        canvas = canvas.Canvas("/tmp/form.pdf", pagesize=letter)
        canvas.setLineWidth(.3)
        canvas.setFont('Helvetica', 12)

        canvas.drawString(30, 750, 'REGALOS S.A de CV')
        canvas.drawString(30, 735, 'FACTURA #%s' % random.randint(1, 1000))
        canvas.drawString(500, 750, today)
        canvas.line(480, 747, 580, 747)

        canvas.drawString(30, 703, 'RFC de REGALOS S.A de CV:')
        canvas.drawString(230, 703, "SAVR090503795")

        canvas.drawString(30, 683, 'Direccion de REGALOS S.A de CV:')
        canvas.drawString(230, 683, "AV JUAREZ NO. 907, PERIODISTAS, 42000, Pachuca, HIDALGO")

        canvas.drawString(30, 643, 'Nombre:')
        canvas.drawString(230, 643, "Mauricio Mejia")

        canvas.drawString(30, 623, 'RFC:')
        canvas.drawString(230, 623, "MERM971214HDFJMKR07")

        canvas.drawString(30, 603, 'Direcciom:')
        canvas.drawString(230, 603, "Calle 28 133 Progreso Nacional")

        canvas.drawString(30, 583, 'Importe:')
        canvas.drawString(230, 583, "20")

        canvas.drawString(30, 563, 'IVA:')
        canvas.drawString(230, 563, "20")

        canvas.drawString(30, 543, 'TOTAL:')
        canvas.drawString(230, 543, "20")

        canvas.save()

        email = EmailMessage()
        email.subject = "New shirt submitted"
        email.body = "Tu factura esta lista"
        email.from_email = "cuentatest997@gmail.com"
        email.to = ["mauriciodinki@gmail.com", ]
        email.attach_file("/tmp/form.pdf")  # Attach a file directly
        email.send()

        return TemplateResponse(request, 'users/profile.html', context)


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return super(LoginView, self).form_valid(form)


class SignupView(RequestFormMixin, FormView):
    template_name = 'auth/signup.html'
    form_class = SignupForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        login(self.request, form.user_cache)
        return super(SignupView, self).form_valid(form)


@login_required(login_url=reverse_lazy('users:login'))
def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('info:home'))