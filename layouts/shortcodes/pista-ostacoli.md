| Ostacolo | Posizione | Distanza dalla soglia |
|---|---|---|
{{ range site.Params.runway.obstacles -}}
| {{ .name }} | {{ .position }} | {{ .distance }} |
{{ end -}}
