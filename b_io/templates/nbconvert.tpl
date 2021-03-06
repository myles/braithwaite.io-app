{%- extends 'display_priority.tpl' -%}

{% block codecell %}
  {%- if not (cell.metadata.hide_output or nb.metadata.hide_input or cell.metadata.hide_input) -%}
  <div class="c-jupyter__row c-jupyter__row--code">
    {{ super() }}
  </div>
  {% endif %}
{%- endblock codecell %}

{% block input_group -%}
  <div class="c-jupyter__input">
    {{ super() }}
  </div>
{% endblock input_group %}

{% block output_group %}
<div class="c-jupyter__output">
  {{ super() }}
</div>
{% endblock output_group %}

{% block in_prompt -%}
<div class="c-jupyter__prompt c-jupyter__prompt--input">
    {%- if cell.execution_count is defined -%}
        In&nbsp;[{{ cell.execution_count|replace(None, "&nbsp;") }}]:
    {%- else -%}
        In&nbsp;[&nbsp;]:
    {%- endif -%}
</div>
{%- endblock in_prompt %}

{% block empty_in_prompt -%}
<div class="c-jupyter__prompt c-jupyter__prompt--input c-jupyter__prompt--empty">
  &nbsp;
</div>
{%- endblock empty_in_prompt %}

{#
  output_prompt doesn't do anything in HTML,
  because there is a prompt div in each output area (see output block)
#}
{% block output_prompt %}
{% endblock output_prompt %}

{% block input %}
<div class="c-jupyter__cell c-jupyter__cell--input">
  {{ cell.source | highlight_code(metadata=cell.metadata) }}
</div>
{%- endblock input %}

{% block output_area_prompt %}
{%- if output.output_type == 'execute_result' -%}
    <div class="c-jupyter__prompt c-jupyter__prompt--output">
    {%- if cell.execution_count is defined -%}
        Out[{{ cell.execution_count|replace(None, "&nbsp;") }}]:
    {%- else -%}
        Out[&nbsp;]:
    {%- endif -%}
{%- else -%}
    <div class="c-jupyter__prompt">
        &nbsp;
{%- endif -%}
    </div>
{% endblock output_area_prompt %}

{% block output %}
{% if resources.global_content_filter.include_output_prompt %}
    {{ self.output_area_prompt() }}
{% endif %}
{{ super() }}
{% endblock output %}

{% block markdowncell scoped %}
<div class="c-jupyter__row c-jupyter__row--text c-jupyter__row--border-box-sizing c-jupyter__row--rendered">
  {%- if resources.global_content_filter.include_input_prompt-%}
  {{ self.empty_in_prompt() }}
  {%- endif -%}
  <div class="c-jupyter__cell c-jupyter__cell--input">
    {{ cell.source  | markdown2html | strip_files_prefix }}
  </div>
</div>
{%- endblock markdowncell %}

{% block unknowncell scoped %}
unknown type  {{ cell.type }}
{% endblock unknowncell %}

{% block execute_result -%}
{%- set extra_class="output_execute_result" -%}
{% block data_priority scoped %}
{{ super() }}
{% endblock data_priority %}
{%- set extra_class="" -%}
{%- endblock execute_result %}

{% block stream_stdout -%}
<div class="c-jupyter__cell c-jupyter__cell--output c-jupyter__cell--output-subarea c-jupyter__cell--output-stream c-jupyter__cell--output-stdout c-jupyter__cell--output-text">
<pre>
{{- output.text | ansi2html -}}
</pre>
</div>
{%- endblock stream_stdout %}

{% block stream_stderr -%}
<div class="c-jupyter__cell c-jupyter__cell--output c-jupyter__cell--output-subarea c-jupyter__cell--output-stream c-jupyter__cell--output-stderr c-jupyter__cell--output-text">
<pre>
{{- output.text | ansi2html -}}
</pre>
</div>
{%- endblock stream_stderr %}

{% block data_svg scoped -%}
<div class="c-jupyter__cell c-jupyter__cell--output c-jupyter__cell--output-svg c-jupyter__cell--output-subarea {{ extra_class }}">
{%- if output.svg_filename %}
<img src="{{ output.svg_filename | posix_path }}"
{%- else %}
{{ output.data['image/svg+xml'] }}
{%- endif %}
</div>
{%- endblock data_svg %}

{% block data_html scoped -%}
<div class="c-jupyter__cell c-jupyter__cell--output c-jupyter__cell--output-html c-jupyter__cell--rendered-html c-jupyter__cell--output-subarea {{ extra_class }}">
{{ output.data['text/html'] }}
</div>
{%- endblock data_html %}

{% block data_markdown scoped -%}
<div class="c-jupyter__cell c-jupyter__cell--output c-jupyter__cell--output-markdown c-jupyter__cell--rendered-html c-jupyter__cell--output-subarea {{ extra_class }}">
{{ output.data['text/markdown'] | markdown2html }}
</div>
{%- endblock data_markdown %}

{% block data_png scoped %}
<div class="c-jupyter__cell c-jupyter__cell--output c-jupyter__cell--output-png c-jupyter__cell--output-subarea {{ extra_class }}">
{%- if 'image/png' in output.metadata.get('filenames', {}) %}
<img src="{{ output.metadata.filenames['image/png'] | posix_path }}"
{%- else %}
<img src="data:image/png;base64,{{ output.data['image/png'] }}"
{%- endif %}
{%- set width=output | get_metadata('width', 'image/png') -%}
{%- if width is not none %}
width={{ width }}
{%- endif %}
{%- set height=output | get_metadata('height', 'image/png') -%}
{%- if height is not none %}
height={{ height }}
{%- endif %}
{%- if output | get_metadata('unconfined', 'image/png') %}
class="unconfined"
{%- endif %}
>
</div>
{%- endblock data_png %}

{% block data_jpg scoped %}
<div class="c-jupyter__cell c-jupyter__cell--output c-jupyter__cell--output-jpeg c-jupyter__cell--output-subarea {{ extra_class }}">
{%- if 'image/jpeg' in output.metadata.get('filenames', {}) %}
<img src="{{ output.metadata.filenames['image/jpeg'] | posix_path }}"
{%- else %}
<img src="data:image/jpeg;base64,{{ output.data['image/jpeg'] }}"
{%- endif %}
{%- set width=output | get_metadata('width', 'image/jpeg') -%}
{%- if width is not none %}
width={{ width }}
{%- endif %}
{%- set height=output | get_metadata('height', 'image/jpeg') -%}
{%- if height is not none %}
height={{ height }}
{%- endif %}
{%- if output | get_metadata('unconfined', 'image/jpeg') %}
class="unconfined"
{%- endif %}
>
</div>
{%- endblock data_jpg %}

{% block data_latex scoped %}
<div class="c-jupyter__cell c-jupyter__cell--output c-jupyter__cell--output-latex c-jupyter__cell--output-subarea {{ extra_class }}">
{{ output.data['text/latex'] }}
</div>
{%- endblock data_latex %}

{% block error -%}
<div class="c-jupyter__cell c-jupyter__cell--output c-jupyter__cell--output-subarea c-jupyter__cell--output-text c-jupyter__cell--output-error">
<pre>
{{- super() -}}
</pre>
</div>
{%- endblock error %}

{%- block traceback_line %}
{{ line | ansi2html }}
{%- endblock traceback_line %}

{%- block data_text scoped %}
<div class="c-jupyter__cell c-jupyter__cell--output c-jupyter__cell--output-text c-jupyter__cell--output-subarea {{ extra_class }}">
<pre>
{{- output.data['text/plain'] | ansi2html -}}
</pre>
</div>
{%- endblock -%}

{%- block data_javascript scoped %}
{% set div_id = uuid4() %}
<div id="{{ div_id }}"></div>
<div class="c-jupyter__cell c-jupyter__cell--output c-jupyter__cell--output-subarea c-jupyter__cell--output-javascript {{ extra_class }}">
<script type="text/javascript">
var element = $('#{{ div_id }}');
{{ output.data['application/javascript'] }}
</script>
</div>
{%- endblock -%}

{%- block data_widget_state scoped %}
{% set div_id = uuid4() %}
{% set datatype_list = output.data | filter_data_type %}
{% set datatype = datatype_list[0]%}
<div id="{{ div_id }}"></div>
<div class="output_subarea output_widget_state {{ extra_class }}">
<script type="text/javascript">
var element = $('#{{ div_id }}');
</script>
<script type="{{ datatype }}">
{{ output.data[datatype] | json_dumps }}
</script>
</div>
{%- endblock data_widget_state -%}

{%- block data_widget_view scoped %}
{% set div_id = uuid4() %}
{% set datatype_list = output.data | filter_data_type %}
{% set datatype = datatype_list[0]%}
<div id="{{ div_id }}"></div>
<div class="output_subarea output_widget_view {{ extra_class }}">
<script type="text/javascript">
var element = $('#{{ div_id }}');
</script>
<script type="{{ datatype }}">
{{ output.data[datatype] | json_dumps }}
</script>
</div>
{%- endblock data_widget_view -%}

{%- block footer %}
{% set mimetype = 'application/vnd.jupyter.widget-state+json'%}
{% if mimetype in nb.metadata.get("widgets",{})%}
<script type="{{ mimetype }}">
{{ nb.metadata.widgets[mimetype] | json_dumps }}
</script>
{% endif %}
{{ super() }}
{%- endblock footer-%}
