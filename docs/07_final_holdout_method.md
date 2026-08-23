# Final VAT Discovery and Attribution Method

## Purpose

This document freezes the discovery, verification and attribution method
after the ten-company development sample.

The same method will be applied to all 30 holdout companies without
company-specific changes.

## Development results

The development sample contained 10 companies.

- VAT candidates found: 3
- HMRC-valid candidates: 3
- Accepted company-to-VAT relationships: 2
- HMRC-valid candidate attributed to the wrong entity: 1
- Companies with no public candidate found: 7

The observed candidate-level wrong-entity rate was 1 out of 3 candidates.

This is a small diagnostic sample and is not treated as a stable population
estimate.

## Stage 1: Confirm the target company

For each company:

1. use the frozen Companies House number as the target identifier;
2. confirm that the Companies House record exists;
3. compare the sampled name with the Companies House legal name;
4. record the company status and registered office.

A plausible identifier format is not sufficient on its own.

If the Companies House number belongs to a different entity, the case is
stopped and recorded as an input-identity failure.

## Stage 2: Resolve and confirm the official domain

Domain candidates may come from:

1. the OCDS supplier `details.url` field;
2. an email domain in the OCDS supplier object;
3. the supplier website displayed in Find a Tender;
4. a controlled web search using the legal name and Companies House number.

A domain is confirmed when the website displays at least one strong legal
identifier:

- the exact Companies House number;
- the legal company name and a compatible address;
- an explicit statement connecting the trading name to the target legal
  entity.

A matching brand name alone is not sufficient.

## Stage 3: Search for VAT candidates

Search the confirmed official domain in the following order:

1. homepage and footer;
2. Terms and Conditions;
3. Legal Notice;
4. Privacy Policy;
5. Contact and About pages;
6. other clearly relevant commercial or legal pages;
7. directly linked public PDFs likely to contain company or invoicing
   information.

The search terms are:

- VAT
- VAT number
- VAT No
- VAT registration
- VAT Reg
- GB followed by a possible nine-digit identifier

Large collections of unrelated governance or employment policies will not
be inspected exhaustively unless a specific document appears commercially
relevant.

This rule was added because large policy collections in the development
sample produced no VAT candidates and had low marginal value.

## Stage 4: Record candidates without accepting them

For every candidate, record:

- target company name;
- Companies House number;
- candidate VAT number;
- exact source URL;
- exact source text;
- source type;
- date observed.

A candidate is not considered correct because it:

- has nine digits;
- passes a checksum;
- appears on an official website;
- is labelled as a VAT number;
- is confirmed as valid by HMRC.

## Stage 5: Verify every candidate with HMRC

Every candidate must be checked using the HMRC UK VAT number checker.

Record exactly:

- valid or invalid;
- registered business name;
- registered business address;
- date and time of the check.

Candidates that are not checked with HMRC do not count as found VAT
relationships.

## Stage 6: Attribute the VAT registration

### Accept

Accept the relationship when:

1. the candidate comes from a confirmed official domain;
2. HMRC confirms that the number is valid;
3. the HMRC registered name is exact or legally equivalent to the target
   company name;
4. there is no evidence that the number belongs to another entity.

`Ltd` and `Limited` are treated as equivalent legal suffixes.

An address difference is recorded but does not automatically cause rejection
when the legal name and company-domain evidence are strong.

### Manual review

Use manual review when:

- HMRC returns a parent or group company;
- the website is operated under a trading name;
- a VAT group may be involved;
- the target is an overseas company or establishment;
- the name relationship is plausible but not demonstrated;
- different public sources provide conflicting entity evidence.

### Reject

Reject the candidate when:

- HMRC reports it as invalid;
- HMRC returns an unrelated legal entity;
- the domain cannot be connected to the target company;
- the source appears historical and the current relationship cannot be
  demonstrated.

A valid number belonging to another entity is classified as:

`valid_wrong_entity`

## Stage 7: Record missing results precisely

Use one of the following outcomes:

- `no_confirmed_domain`
- `domain_unreachable`
- `no_candidate_found`
- `candidate_hmrc_invalid`
- `valid_wrong_entity`
- `manual_review`
- `accept`

`no_candidate_found` means that the checked public sources did not expose a
candidate. It does not mean that the company is not VAT registered.

## Holdout restrictions

During the holdout evaluation:

- companies will not be replaced;
- the search order will not be changed for individual companies;
- new source families will not be introduced selectively;
- unsuccessful searches will remain in the denominator;
- every discovered candidate will be checked with HMRC;
- all accepted results will retain source and verification evidence.

If a major previously unknown failure mode is discovered, it will be
documented separately. The original holdout results will not be silently
rewritten.