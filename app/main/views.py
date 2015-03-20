from flask import render_template, request, redirect
from . import main
from .helpers.validation_tools import Validate
from .helpers.content import ContentLoader
from .helpers.service import ServiceLoader
from .helpers.presenters import Presenters
from .helpers.s3 import S3


content = ContentLoader(
    "app/section_order.yml",
    "bower_components/digital-marketplace-ssp-content/g6/"
)
presenters = Presenters()


@main.route('/')
def index():
    return render_template("index.html", **get_template_data())


@main.route('/service')
def find():
    return redirect("/service/" + request.args.get("service_id"))


@main.route('/service/<service_id>')
def view(service_id):
    service_loader = ServiceLoader(
        main.config['API_URL'],
        main.config['API_AUTH_TOKEN'],
    )
    service_data = service_loader.get(service_id)
    presented_service_data = {}
    for key, value in service_data.items():
        presented_service_data[key] = presenters.present(
            value, content.get_question(key)
        )

    template_data = get_template_data({
        "sections": content.sections,
        "service_data": presented_service_data,
        "service_id": service_id
    })
    return render_template("view_service.html", **template_data)


@main.route('/service/<service_id>/edit/<section>')
def edit(service_id, section):
    service_loader = ServiceLoader(
        main.config['API_URL'],
        main.config['API_AUTH_TOKEN'],
    )

    template_data = get_template_data({
        "section": content.get_section(section),
        "service_data": service_loader.get(service_id),
    })
    return render_template("edit_section.html", **template_data)


@main.route('/service/<service_id>/edit/<section>', methods=['POST'])
def update(service_id, section):
    service_loader = ServiceLoader(
        main.config['API_URL'],
        main.config['API_AUTH_TOKEN'],
    )

    s3_uploader = S3(
        bucket_name=main.config['S3_DOCUMENT_BUCKET'],
    )

    service = service_loader.get(service_id)
    posted_data = dict(
        list(request.form.items()) + list(request.files.items())
    )

    errors = Validate(content, service, posted_data, s3_uploader).errors

    for question_id in posted_data:
        if question_id not in errors:
            service_loader.set(service, question_id, "new value")

    service_loader.post(service)

    if errors:
        return render_template("edit_section.html", **get_template_data({
            "section": content.get_section(section),
            "service_data": service,
            "edits_submitted": posted_data,
            "service_id": service_id,
            "errors": errors
        }))
    else:
        return redirect("/service/" + service_id)


def get_template_data(merged_with={}):
    return dict(main.config['BASE_TEMPLATE_DATA'], **merged_with)
