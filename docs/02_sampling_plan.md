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