## About the Project
**Project Title: Grazioso Salvare Rescue Dog Dashboard**

Grazioso Salvare trains dogs for search-and-rescue work. This project gives their staff a web dashboard for searching about 10,000 animal shelter 
outcome records from the Austin Animal Center. One click narrows the list to dogs that fit a specific kind of rescue training 
(water, mountain or wilderness, or disaster and individual tracking). The table, a breed pie chart, and a location map all update to match.

The stack is MongoDB for storage, a reusable Python CRUD module (built in Project One) for every database call, and a Dash application 
(built in Project Two) for the interface.

## Repository Contents

| File | What it is |
|------|------------|
| `ProjectTwoDashboard.ipynb` | The final Dash dashboard: filters, data table, pie chart, and geolocation map |
| `CRUD_Python_Module.py` | The `AnimalShelter` class from Project One that handles Create, Read, Update, and Delete against MongoDB |
| `Grazioso Salvare Logo.png` | Client logo shown in the dashboard header |
| `CS_340_MODULE_SEVEN_README_ASSIGNMENT.docx` | The full Project Two README with screenshots, setup steps, tool rationale, and the problems I worked through |

To run it, put the three code and image files in one folder, set the `aacuser` credentials in the notebook's data-load cell, and run all cells. The Word document has the complete setup instructions.

## Reflection

### How do you write programs that are maintainable, readable, and adaptable?

For me it mostly comes down to deciding where each responsibility lives and then not letting it leak anywhere else. The CRUD module from Project One is 
the clearest example. Every conversation with MongoDB goes through the `AnimalShelter` class. The dashboard never imports PyMongo, never builds a 
connection string, and never handles a driver exception. It asks for records and gets back a plain Python list.

That separation paid off in Project Two more than I expected. When I started building the dashboard, I didn't have to think about authentication, 
timeouts, or what happens when a query fails, because those questions had already been answered once, in one file. I could focus entirely on the layout 
and callbacks. When something did break, the boundary made it easy to tell which side the problem was on. If `db.read()` returned the right count in a plain 
notebook cell, the bug was in the dashboard, not the database.

**A few habits made the module itself easier to live with:**

- **Defaults with room to override.** The constructor defaults to the Codio host, port, database, and collection, but every one of those is a parameter.
                                      Pointing the class at a different server or collection doesn't require editing the class.
- **Safety where mistakes are expensive.** `update()` and `delete()` refuse an empty filter, because `{}` matches every document and one slip could
                                            wipe the collection. `read()` allows it because reading everything is harmless.
- **Comments that explain why, not what.** Anyone can see that the code calls `insert_one(dict(data))`. The comment explains that the copy is there
                                           because PyMongo adds an `_id` to the dictionary it's given, which would surprise the caller later.
- **Predictable return values.** Create returns True or False, read always returns a list (empty if nothing matched), and update and delete return a count.
                                 Calling code never has to guess.

I carried the same thinking into the dashboard. The three rescue profiles live in one `RESCUE_PROFILES` dictionary, and one `build_query()` function turns 
any of them into a MongoDB filter. The radio button labels come from that same dictionary. If Grazioso Salvare decides to add a breed or change an age 
range, they edit one entry, and the query and the button can't fall out of sync.

As for future use, the module isn't really tied to dogs or to this dashboard. It could back a command-line tool for shelter staff, a scheduled script that 
flags new animals matching a rescue profile and emails the trainers, a REST API built with Flask or FastAPI, or a completely different collection with 
different data. Because the database and collection names are constructor arguments, reusing it for another project is mostly a matter of passing different 
values.

### How do you approach a problem as a computer scientist?

I try to understand what the client actually needs before I write anything, and then I build in small pieces that I can prove work before the next piece 
depends on them.

Grazioso Salvare's requirements were specific: certain breeds, a certain sex, and an age window in weeks for each rescue type. Before touching the 
interface, I translated each profile into a MongoDB query and ran all of them in a plain notebook cell. The counts came back as 17, 5, 4, and 10,000. 
That gave me a fixed point to test against. Every time I changed the dashboard afterward, I could check the on-screen numbers against those results.

Those small numbers also taught me something about treating unexpected results as questions instead of bugs. Seventeen dogs out of thousands looked 
wrong at first. Checking each condition separately showed the query was correct. Requiring an intact animal removes every spayed or neutered dog, and 
combined with breed and age, the pool gets small fast. That's information the client can use, so I documented it rather than "fixing" it.

This project felt different from earlier coursework. In most previous assignments, the problem arrived already broken down: write this function, pass 
these tests, done. Here there was a client, a specification document, and a set of deliverables that had to work together. The database layer had to be 
built well enough to survive a second project I hadn't seen yet. I also had to think about the people using it. Radio buttons made more sense than a 
dropdown because the rescue types are mutually exclusive and should all be visible at once. A pie chart with hundreds of breed slices is technically 
correct and practically useless, so I grouped everything past the top eight into "Other."

For future client databases, I'd keep doing what worked and add a few things:

- Start with the questions the client needs answered, then design the documents and indexes around those queries.
- Build the data access layer first, test it on its own, and only then put an interface on top.
- Keep business rules (like rescue profiles) as data instead of hard-coding them into logic.
- Create restricted database users from the start, with only the permissions the application needs.
- Write down the decisions and the dead ends while they're fresh, because they're the first thing anyone maintaining the project will want to know.

### What do computer scientists do, and why does it matter?

At its best, computer science takes something people are doing slowly, manually, or not at all, and makes it fast, reliable, and repeatable. A lot of that 
work is invisible when it's done right. Nobody using this dashboard will ever see the CRUD module, the indexes, or the role-based permissions, and that's 
the point. They just see a list of dogs that fit the job.

For Grazioso Salvare, the alternative to this dashboard is a trainer scrolling through a spreadsheet of 10,000 rows, mentally checking breed, sex, and age 
for each one. That's hours of tedious work with plenty of room for mistakes, and every hour spent on it is an hour not spent training dogs. With the 
dashboard, the same search takes one click and gives the same answer every time. The map shows where each candidate is, so staff can plan pickups. The pie 
chart shows at a glance what breeds are available.

There's also a longer-term benefit. Because the profiles are stored as data and the database code is reusable, the system can grow with the organization. If 
they add a new type of rescue work, partner with more shelters, or want reports on which breeds succeed in training, the foundation is already there. Good 
software helps an organization do today's work better and leaves room for the work they haven't thought of yet. For a group whose job is finding people in 
emergencies, getting the right dogs into training sooner matters well beyond the code.

---

**Data source:** Austin Animal Center. (2020). *Austin Animal Center Outcomes* [Data set]. City of Austin, Texas Open Data Portal. https://doi.org/10.26000/025.000001
