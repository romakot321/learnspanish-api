from app.db.tables import Lesson
from sqladmin import ModelView

from sqladmin.formatters import Markup


def format_file_url(model, attribute) -> Markup:
    return Markup(f'<audio controls><source src="/api/lesson/{model.id}" type="audio/wav"></audio>')


def format_image_url(model, attribute) -> Markup:
    if getattr(model, attribute) is None:
        return Markup("<div></div>")
    return Markup(
        f'<img src="/{getattr(model, attribute)}" />'
    )


class LessonView(ModelView, model=Lesson):
    column_list = [Lesson.title, Lesson.preview, Lesson.level, Lesson.id]
    column_searchable_list = [Lesson.id, Lesson.title]
    column_default_sort = [(Lesson.created_at, True)]
    column_sortable_list = [Lesson.level]
    column_formatters_detail = {"file": format_file_url, "text_file": format_file_url, "image": format_image_url}
    column_formatters = {"image": format_image_url}

