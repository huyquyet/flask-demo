__author__ = 'FRAMGIA\nguyen.huy.quyet'

from flask import Blueprint, render_template, flash, url_for, redirect, Markup

from .forms import SiteForm, VisitForm
from .models import db, query_to_list, Site, Visit

flask = Blueprint("flask", __name__)


@flask.route("/")
def index():
    site_form = SiteForm()
    visit_form = VisitForm()
    return render_template("index.html", site_form=site_form, visit_form=visit_form)


@flask.route("/site", methods=("POST",))
def add_site():
    form = SiteForm()
    if form.validate_on_submit():
        site = Site()
        form.populate_obj(site)
        db.session.add(site)
        db.session.commit()
        flash("Added site")
        return redirect(url_for(".index"))
    return render_template("Validation_error.html", form=form)


@flask.route("/site/<int:site_id>")
def view_site_visits(site_id=None):
    site = Site.query.get_or_404(site_id)
    query = Visit.query.filter(Visit.site_id == site_id)
    data = query_to_list(query)
    title = "Visits for {}".format(site.base_url)
    return render_template("data_list.html", data=data, title=title)


@flask.route("/visit", methods=("POST",))
@flask.route("/site/<int:site_id>/visit", methods=("POST",))
def add_visit(site_id=None):
    if site_id is None:
        # This is only used by the visit_form on the index page.
        form = VisitForm()
    else:
        site = Site.query.get_or_404(site_id)
        # WTForms does not coerce obj or keyword arguments
        # (otherwise, we could just pass in `site=site_id`)
        # CSRF is disabled in this case because we will *want*
        # users to be able to hit the /site/:id endpoint from other sites.
        form = VisitForm(csrf_enabled=False, site=site)

    if form.validate_on_submit():
        visit = Visit()
        form.populate_obj(visit)
        visit.site_id = form.site.data.id
        db.session.add(visit)
        db.session.commit()
        flash("Added visit for site {}".format(form.site.data.base_url))
        return redirect(url_for(".index"))

    return render_template("validation_error.html", form=form)


@flask.route("/sites")
def view_sites():
    query = Site.query.filter(Site.id >= 0)
    data = query_to_list(query)

    # The header row should not be linked
    results = [next(data)]
    for row in data:
        row = [_make_link(cell) if i == 0 else cell
               for i, cell in enumerate(row)]
        results.append(row)

    return render_template("data_list.html", data=results, title="Sites")


_LINK = Markup('<a href="{url}">{name}</a>')


def _make_link(site_id):
    url = url_for(".view_site_visits", site_id=site_id)
    return _LINK.format(url=url, name=site_id)
