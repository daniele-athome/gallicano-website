---
title: "La pista"
description: "Scheda operativa RM24: dati pista, sequenza di arrivo, circuito, ostacoli e limitazioni."
showInfoStrip: true
---

| Identificazione | |
|---|---|
| Codice | {{< param "runway.code" >}} ([Avioportolano]({{< param "runway.avioportolanoUrl" >}})) |
| Località | {{< param "runway.locality" >}} |
| Coordinate | [{{< param "runway.coordinates" >}}]({{< param "runway.mapsUrl" >}}) |
| Elevazione | {{< param "runway.elevation" >}} |
| Stato | {{< param "runway.status" >}} |

| Pista | |
|---|---|
| **Orientamento** | **{{< param "runway.orientation" >}}** |
| Dimensioni | {{< param "runway.dimensions" >}} |
| Superficie | {{< param "runway.surface" >}} |
| Pendenza | {{< param "runway.slope" >}} |
| Maniche a vento | {{< param "runway.windsocks" >}} |

| Radio e operatività | |
|---|---|
| Frequenza | {{< param "runway.frequency" >}} — autoinformazione |
| Servizio di controllo | {{< param "runway.radioService" >}} |
| Orari | {{< param "runway.hours" >}} |
| Preavviso | {{< param "runway.priorNotice" >}} |
| **Traffico ammesso** | **{{< param "runway.trafficAllowed" >}}** |
| Scuola di volo | {{< param "runway.flightSchool" >}} |
| Spazio aereo | {{< param "runway.airspace" >}} |
| Meteo in campo | [meteo.aviocaipoli.it]({{< param weatherUrl >}}) |

## In arrivo

1. **{{< param "runway.reportingRange" >}}** — riporto in frequenza: posizione, quota, testata prevista.
2. **Ascolto** — nessun controllo, il coordinamento è tra gli equipaggi.
3. **Sottovento** — {{< param "runway.circuitAltitude" >}} ({{< param "runway.circuitHeight" >}} sul campo), sempre a {{< param "runway.circuitSide" >}} della pista.
4. **Finale** — profilo di discesa normale, non anticipare la soglia.
5. **Dopo l'atterraggio** — liberare la pista, parcheggio sul lato est.

## Circuito

{{% pista-circuito %}}

Entrambi i circuiti si sviluppano a **{{< param "runway.circuitSide" >}}**.

## Ostacoli

{{% pista-ostacoli %}}

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

## Il campo dall'alto

![Finale per pista 14](/images/pista/14-finale.jpg)
*14 — finale. Gallicano sulla sinistra, filare di alberi sulla soglia.*

![Il campo dalla testata 14](/images/pista/14-obliqua.jpg)
*14 — obliqua. Pista, maniche a vento, parcheggio sul lato ovest.*

![Finale per pista 32](/images/pista/32-finale.jpg)
*32 — finale. Linea elettrica trasversale, strada comunale oltre.*

![Il campo dalla testata 32](/images/pista/32-obliqua.jpg)
*32 — obliqua. Il circuito si sviluppa sul lato in basso a destra.*

Informazioni e stato del campo: [contatti]({{< relref "contatti" >}}).
