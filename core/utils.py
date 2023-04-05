import weasyprint
from django.shortcuts import HttpResponse
from django.template.loader import render_to_string


def pdf_generation(request, context, pdf_name):
    html = render_to_string('core/motagra_report.html',
                            context)
    response = HttpResponse(content_type='application/pdf')
    encoded_pdf_name = pdf_name.encode('utf-8').decode('ISO-8859-1')
    response['Content-Disposition'] = f'filename={encoded_pdf_name}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, )
    return response
