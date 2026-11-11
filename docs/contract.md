# Plug-in contract

> This is the specification you give the coding agent, and the document a
> third party would need to write a plug-in for your core without reading the
> core's code. Fill it in **before** you generate any core code. Commit it
> and tag the commit `contract-v1`. Delete the quoted guidance when you are
> done.

Group: …
Members: …

## 1. Responsibilities of the core

> What the core does, and what it deliberately does not do. Keep the list
> short: everything on it is code that every future change may have to touch.

## 2. What a plug-in is

> Form (a file, a folder, a class …), name and description, where it lives.

## 3. Interface

> The operations a plug-in offers to the core and the core offers to a
> plug-in, with types. What does a plug-in receive, and what does it return?

## 4. Discovery and registration

> How the core finds plug-ins at run time, and what makes a file a valid
> plug-in. What happens with files that are not plug-ins?

## 5. Life cycle

> When a plug-in is loaded, initialised, called and released. Is a plug-in
> called once per run or once per text? May it keep state?

## 6. Errors

> What a plug-in does when it cannot process a text, and what the core does
> then. What the core does with a plug-in that cannot be loaded.

## 7. What a plug-in may and may not do

> Access to files, to the network, to other plug-ins, to the core's
> internals. How is this enforced, or is it only a convention?

## 8. Versioning

> How a plug-in and the core find out that they fit together. What happens to
> existing plug-ins when the contract changes?

## Decisions taken by the agent

> If the coding agent had to decide something this document left open, it
> lists the decision here, so that you can review it.

## Changes after `contract-v1`

> Leave empty at first. List every change to the contract with the date, the
> extension request that caused it, and whether existing plug-ins had to be
> changed.

| Date | Change | Caused by | Existing plug-ins changed? |
|------|--------|-----------|----------------------------|
