Cresta Flow
-----------
(email: danwgrace@gmail.com)

Version 1.0

Cresta Flow is an open source skeleton / framework for a web based workflow
management system.  It allows any simple workflow model to be implemented.  This
is achieved by modelling workflow items as a graph of states and transitions.
A workflow item is in a particular state at any point in time.  Depending on
input from a user the state of the workflow item may be advanced to some other
state.  Typically in most practical applications when a workflow item is
advanced additional custom information is required from the user.  Each user of
the workflow system belongs to one or more groups.  For each group there is set
of states which determine which workflow items are currently visible.  Also
defined are a list of initial states and a list of terminal states (states that
have no further transitions).  Initial and terminal states can be used to
calculate the active duration of a workflow item.  The system supports multiple
workflow types, which are mutually exclusive.

The code presented here is not intended to be used as is.  It is configured for
a particular example workflow system where there are four states (1, 2, 3, 4)
and two user groups (1, 2).  From the initial state (1) a workflow item may only
be advanced to state 2.  From state 2 a workflow item may be advance either of
the terminal states 3 or 4.  When implementing this system the states and groups
should be given more descriptive names.  There are two demo custom forms
included custom form A and custom form B.  Custom form A is displayed when
advancing from state 1 and custom form B is displayed when advancing from state
2.

To specify a workflow system edit the "init" method of the "Workflow" class in
"utils.py".  To specify custom forms, displayed when advancing workflow items,
edit the "advance_flow" function in "views.py".  Also edit the custom form
definitions in "forms.py".  The "setupdb.py" script needs to be edited so that
it includes the appropriate types, states and groups to match with the "init"
method of the "Workflow" class.  Then the database can be initialised before the
system is used, by running the "setupdb.py" script.  The list flows page
includes a template tag function for colouring the rows based on the flow data,
which should be changed as required.  The system is in debug mode, be sure to
turn off debugging and enable logging before using in a production environment.

The system was developed using the following tools / versions:
Django==1.7.1
Pillow==2.6.1
psycopg2==2.5.4
pytz==2014.10

See gpl-2.0.txt for license details!
