---
title: "La pista"
description: "Scheda operativa RM24: dati pista, sequenza di arrivo, circuito, ostacoli e limitazioni."
showInfoStrip: true
heroImage: "foto/aeree/32-panoramica.jpg"
heroImagePosition: "center 40%"
---

![Schema pista e circuiti](images/pista/runway-patterns.svg)

| Identificazione |                                                                                        |
|-----------------|----------------------------------------------------------------------------------------|
| Codice          | {{< param "runway.code" >}} ([Avioportolano]({{< param "runway.avioportolanoUrl" >}})) |
| Località        | {{< param "runway.locality" >}}                                                        |
| Coordinate      | [{{< param "runway.coordinates" >}}]({{< param "runway.mapsUrl" >}})                   |
| Elevazione      | {{< param "runway.elevation" >}}                                                       |

| Pista            |                                        |
|------------------|----------------------------------------|
| **Orientamento** | **{{< param "runway.orientation" >}}** |
| Dimensioni       | {{< param "runway.dimensions" >}}      |
| Superficie       | {{< param "runway.surface" >}}         |
| Pendenza         | {{< param "runway.slope" >}}           |
| Maniche a vento  | {{< param "runway.windsocks" >}}       |

| Radio e operatività   |                                                     |
|-----------------------|-----------------------------------------------------|
| Frequenza             | {{< param "runway.frequency" >}} — autoinformazione |
| Servizio di controllo | {{< param "runway.radioService" >}}                 |
| Orari                 | {{< param "runway.hours" >}}                        |
| Preavviso             | {{< param "runway.priorNotice" >}}                  |
| **Traffico ammesso**  | **{{< param "runway.trafficAllowed" >}}**           |
| Scuola di volo        | {{< param "runway.flightSchool" >}}                 |
| Spazio aereo          | {{< param "runway.airspace" >}}                     |
| Meteo in campo        | [meteo.aviocaipoli.it]({{< param weatherUrl >}})    |

## In arrivo

1. **{{< param "runway.reportingRange" >}}** — riporto in frequenza: posizione, quota, testata prevista.
2. **Ascolto** — nessun controllo, il coordinamento è tra gli equipaggi.
3. **Sottovento** — {{< param "runway.circuitAltitude" >}} ({{< param "runway.circuitHeight" >}} sul campo), sempre a {{< param "runway.circuitSide" >}} della pista.
4. **Finale** — profilo di discesa normale, non anticipare la soglia.
5. **Dopo l'atterraggio** — liberare la pista, parcheggio sul lato est.

## Le testate

{{< testate >}}
{{< testata qfu="14" src="foto/aeree/14-finale.jpg" circuito="Destro" >}}
- **Finale libero**, nessun ostacolo sull'asse.
- **Gallicano nel Lazio** davanti a sinistra, sul fianco della collina.
- Hangar e parcheggio sul lato **sinistro**.
- Il circuito si sviluppa sulla **destra** dell'immagine.
{{< /testata >}}
{{< testata qfu="32" src="foto/aeree/32-finale.jpg" circuito="Sinistro" >}}
- **Collinetta a 50 m dalla soglia** — possibili _wind shears_.
- Hangar e parcheggio sul lato **destro**.
- Il circuito si sviluppa sulla **sinistra** dell'immagine.
- Oltre il campo si apre la piana, senza riferimenti vicini.
{{< /testata >}}
{{< /testate >}}

## Circuito

{{% pista-circuito %}}

Entrambi i circuiti si sviluppano a **{{< param "runway.circuitSide" >}}**.

## Ostacoli

{{% pista-ostacoli %}}

{{< foto src="foto/aeree/14-hover.jpg" tipo="aerea" formato="16:9"
         didascalia="La pista **14** dall'alto, con la collinetta sul prolungamento in lontananza." >}}

## Avvertenze

- **Aeroporto militare di Guidonia a 7.3 NM a nord.**
  - ATZ attiva dal lunedì al venerdì, dall'alba al tramonto.
  - Un corridoio in direzione nord a 500 ft AGL è disponibile per ultraleggeri.
  - Il corridoio deve essere attivato ogni giorno chiamando l'aeroporto al telefono.
- TMA Roma da 4000 ft.

## Limitazioni

- Fondo in erba: cedevole dopo piogge prolungate.
- Nessun rifornimento in campo — vedi [servizi]({{< relref "servizi" >}}).
- Nessuna assistenza al volo, nessun servizio antincendio.

{{< foto src="foto/aeree/32-ottobre.jpg" tipo="aerea" formato="16:9" >}}

Informazioni e stato del campo: [contatti]({{< relref "contatti" >}}).
