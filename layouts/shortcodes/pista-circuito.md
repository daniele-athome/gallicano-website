| QFU | Circuito | Note |
|---|---|---|
{{ range site.Params.runway.circuit -}}
| **{{ .runway }}** | {{ .pattern }} | {{ .notes }} |
{{ end -}}
