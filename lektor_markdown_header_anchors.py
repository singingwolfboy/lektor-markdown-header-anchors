from lektor.pluginsystem import Plugin
from lektor.types.formats import MarkdownType
from lektor.utils import slugify
from markupsafe import Markup
from collections import namedtuple


TocEntry = namedtuple('TocEntry', ['anchor', 'title', 'children'])


class MarkdownHeaderAnchorsPlugin(Plugin):
    name = 'Markdown Header Anchors'
    description = 'Adds anchors to markdown headers.'

    def on_markdown_config(self, config, **extra):
        class HeaderAnchorMixin(object):
            def get_header_adjustment(renderer):
                """
                If the model has a `markdown_header_adjustment` option defined
                on a markdown field, return that option value as an integer.
                If not, return 0.
                """
                markdown_fields = [
                    field for field in renderer.record.datamodel.fields
                    if isinstance(field.type, MarkdownType)
                ]
                adjustments = [
                    field.options.get("markdown_header_adjustment")
                    for field in markdown_fields
                    if field.options.get("markdown_header_adjustment")
                ]
                if adjustments:
                    # need a way to figure out which field is being rendered
                    # but for now, arbitrarily take the first one
                    adjustment = adjustments[0]
                    return int(adjustment)
                else:
                    return 0

            def adjusted_header_level(renderer, level):
                """
                Return the adjusted header level as modified by the
                `markdown_header_adjustment` option, bounded between 1 and 6.
                """
                adjustment = renderer.get_header_adjustment()
                return max(1, min(6, level + adjustment))

            def header(renderer, text, level, raw):
                anchor = slugify(raw)
                renderer.meta['toc'].append((level, anchor, Markup(text)))
                return '<h{level:d} id="{anchor}">{text}</h{level:d}>'.format(
                    level=renderer.adjusted_header_level(level),
                    anchor=anchor,
                    text=text,
                )

        config.renderer_mixins.append(HeaderAnchorMixin)

    def on_markdown_meta_init(self, meta, **extra):
        meta['toc'] = []

    def on_markdown_meta_postprocess(self, meta, **extra):
        prev_level = None
        toc = []
        stack = [toc]

        for level, anchor, title in meta['toc']:
            if prev_level is None:
                prev_level = level
            elif prev_level == level - 1:
                stack.append(stack[-1][-1][2])
                prev_level = level
            elif prev_level > level:
                while prev_level > level:
                    stack.pop()
                    prev_level -= 1
            stack[-1].append(TocEntry(anchor, title, []))

        meta['toc'] = toc
