# Sainte-Thérèse (QC)

Waste collection schedules for [Ville de Sainte-Thérèse](https://www.sainte-therese.ca/services/services-aux-citoyens/collectes-et-ecocentre), Québec, Canada.

## Configuration via configuration.yaml

```yaml
waste_collection_schedule:
  sources:
    - name: sainte_therese_qc_ca
      args:
        zone: ZONE
```

### Configuration Variables

**zone**
*(string) (required)*

Collection zone letter: `A`, `B`, `C`, or `D`.

**first_week_collection**
*(string) (optional, default: `recycling`)*

Collection type on the first zone-day of each year. Allowed values:
- `recycling`
- `garbage`

## Example

```yaml
waste_collection_schedule:
  sources:
    - name: sainte_therese_qc_ca
      args:
        zone: A
        first_week_collection: recycling
```

## How to get the source arguments

Use the city collection page and PDF calendar to find your zone:

- https://www.sainte-therese.ca/services/services-aux-citoyens/collectes-et-ecocentre

The city uses 4 zones:
- Zone A: Tuesday
- Zone B: Wednesday
- Zone C: Thursday
- Zone D: Friday
