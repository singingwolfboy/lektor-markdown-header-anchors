# lektor-markdown-header-anchors

This plugin extends the markdown support in Lektor in a way that headlines
are given anchors and a table of contents is collected.

It also allows you to adjust the heading level in the HTML output: converting
all `<h1>` tags to `<h2>` tags, and so on.
This feature should be a separate plugin, but due to the way Lektor plugins
are structured, two plugins that both modify Markdown headers
will clobber each other.

## Enabling the Plugin

To enable the plugin run this command:

```
$ lektor plugins add markdown-header-anchors
```

## In Templates

Within templates it becomes possible to access the `.toc` property of
markdown data.  It's a list where each item has the following attributes:

* `anchor`: the name of the anchor
* `title`: the title of the headline as HTML
* `children`: a list of headers below that header

Example rendering:

```jinja
<h4>Table Of Contents</h4>
<ul class="toc">
{% for item in this.body.toc recursive %}
  <li><a href="#{{ item.anchor }}">{{ item.title }}</a>{%
   if item.children %}<ul>{{ loop(item.children) }}</ul>{% endif %}
{% endfor %}
</ul>
```

## Adjusting Header Levels

To modify the header level of a markdown field, set the
`markdown_header_adjustment` option on that field in the model. For example:

```ini
[fields.body]
label = Body
type = markdown
markdown_header_adjustment = 1
```

This option must be an integer. The value of the integer is added to the level
of the generated header tags in the HTML. With a value of 1, all `<h1>` tags
become `<h2>` tags, and all `<h2>` tags become `<h3>` tags.
With a value of 2, all `<h1>` tags become `<h3>` tags, and all `<h2>` tags
become `<h4>` tags. HTML only defines header tags from `<h1>` to `<h6>`,
so this plugin will bound the output between those two values:
it will never generate an `<h7>` tag, for example.
