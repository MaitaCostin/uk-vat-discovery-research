# Sampling Plan

## Objective

The purpose of the sample is to evaluate whether UK VAT numbers can be
discovered and correctly attributed without selecting companies that are
already known to publish their VAT numbers.

## Target population

The target population is UK companies that supply goods or services to
organisations and may appear in a procurement team's supplier records.

## Sampling frame

The initial sampling frame will consist of UK suppliers named in contract
award notices published on Find a Tender between 1 July 2026 and
31 July 2026.

The sampling frame is chosen before any VAT number searches are performed.

## Eligibility criteria

A supplier is eligible when:

1. it is identified as a UK organisation;
2. it can be connected to a specific Companies House entity;
3. it is a company rather than an individual or sole trader;
4. its Companies House company number can be recorded;
5. it has not already appeared in the sample.

## Exclusion criteria

A supplier will be excluded when:

- it is not based in the UK;
- it is an individual or sole trader;
- no specific Companies House entity can be identified;
- it is a public body, charity, or other organisation outside the scope;
- the same Companies House number has already been selected.

Every exclusion will be recorded with a reason.

## Sample size

The initial proof of concept will use 40 companies:

- 10 companies in a development sample;
- 30 companies in a holdout evaluation sample.

The sample size is intended to test the acquisition process and identify
failure modes. It is not large enough to estimate national VAT coverage
with high statistical confidence.

## Development sample

The development sample will be used to:

- understand the manual discovery process;
- test possible web sources;
- improve extraction rules;
- identify common attribution problems;
- develop the initial pipeline.

Results from the development sample will be reported separately from the
holdout results.

## Holdout sample

The holdout sample will not be used to tune extraction or acceptance rules.

The final pipeline will be applied to the holdout sample after the rules
have been fixed.

## Random selection

Eligible suppliers will be deduplicated by Companies House company number.

The resulting list will be selected using a reproducible random process
with the fixed random seed:

20260818

The first 10 selected companies will form the development sample.

The next 30 selected companies will form the holdout sample.

## Anti-cherry-picking rule

No VAT number search will be performed before the sample has been selected,
saved, and committed to Git.

A company will not be removed or replaced merely because:

- it has no website;
- its website cannot be reached;
- no VAT number is found;
- it does not appear to be VAT registered;
- the company is difficult to investigate.

These are outcomes of the experiment, not valid exclusion reasons.

## Notice batch construction

The sampling frame will initially use the first 20 UK6 contract award notices
published in July 2026, ordered from oldest to newest.

Notice identifiers will be recorded before supplier data is extracted.

No notice will be skipped because it appears incomplete, difficult, or likely
to contain few suppliers.

If the first 20 notices produce fewer than 40 eligible unique Companies House
entities, the next 10 consecutive notices will be added.

Further notices will be added in consecutive blocks of 10 until at least 40
eligible unique companies are available.

This rule prevents notices from being selected based on the availability of
supplier websites, Companies House numbers, or VAT identifiers.

## Sample freeze

Once selected, the sample will be saved in a CSV file and committed to Git.

After the sample is frozen:

- companies will not be replaced based on discovery results;
- all subsequent exclusions or corrections will be documented;
- the development and holdout labels will not be changed.

## Limitations

Suppliers appearing in public procurement notices may differ from the wider
population of UK suppliers.

They may be:

- larger;
- more established;
- more likely to have an official website;
- more likely to publish formal legal information;
- more likely to be VAT registered.

The results will therefore describe performance on this sample and will
not be presented as national VAT coverage.

## First notice batch result

The first 20 consecutive July 2026 UK6 notices were downloaded and
processed successfully.

They produced 26 awarded-supplier rows before deduplication across notices.

Because the total number of supplier rows was already below the required
sample size of 40, the batch could not contain 40 eligible unique companies.

The pre-defined expansion rule was therefore triggered, and the next 10
consecutive notices will be added.

No notice or supplier was removed or replaced based on website availability,
Companies House coverage, or VAT discoverability.

## Thirty-notice batch result

The first 30 consecutive July 2026 UK6 notices produced 46 awarded-supplier
rows.

Of these:

- 22 rows did not contain a Companies House number;
- 24 rows contained a Companies House number;
- those 24 rows represented 22 unique Companies House identifiers;
- 21 unique identifiers had a plausible eight-character format;
- one identifier required review because of its format.

The five-company manual pilot had suggested higher Companies House coverage
than the larger batch. This demonstrated that the pilot was useful as a
source smoke test but was too small to estimate identifier availability.

Even if the identifier requiring review were later validated, the batch
would still contain fewer than 40 eligible unique companies. The review was
therefore deferred, and the predefined rule to add the next 10 consecutive
notices was triggered.

## Forty-notice batch result

The first 40 consecutive July 2026 UK6 contract award notices produced
124 awarded-supplier rows.

Of these:

- 38 rows did not contain a Companies House number;
- 86 rows contained a Companies House number;
- those 86 rows represented 83 unique Companies House identifiers;
- 81 unique identifiers had a plausible eight-character format;
- two identifiers required review.

The 81 plausible unique identifiers were sufficient to construct the
40-company sample. Notice collection was therefore stopped after the
fortieth notice.

The two identifiers requiring review were retained in the source results
but excluded from sample selection. Investigating them could not change
the sampling decision and would introduce unnecessary entity-resolution
risk.

Companies without a website were not excluded. Website availability is
an outcome to be measured during VAT discovery.

## Forty-notice batch result

The first 40 consecutive July 2026 UK6 contract award notices produced
124 awarded-supplier rows.

Of these:

- 38 rows did not contain a Companies House number;
- 86 rows contained a Companies House number;
- these represented 83 unique Companies House identifiers;
- 81 identifiers had a plausible eight-character format;
- two identifiers required review.

The 81 plausible identifiers were sufficient to construct the 40-company
sample. Notice collection was therefore stopped after the fortieth notice.

The two identifiers requiring review were retained in the source results
but excluded from sample selection because investigating them could not
change the sampling decision.