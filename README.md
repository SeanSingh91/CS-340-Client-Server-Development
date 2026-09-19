## About the Project
Project Title: Austin Animal Center CRUD Python Module
This small Python module (CRUD_Python_Module.py) gives Grazioso Salvare's future dashboard a clean way to read and write records in the 
Austin Animal Center MongoDB database, without the rest of the application ever writing a raw Mongo query. AnimalShelter 
currently supports create and read against roughly 10,000 shelter records; update and delete are coming in Project One.
## Motivation
Grazioso Salvare needs to filter thousands of animal records to find dogs fitting its search-and-rescue program, by breed, age, and outcome 
history, and doing that by hand in a spreadsheet does not scale. The plan is a dashboard letting staff browse this data directly, but a dashboard 
is only as good as the layer underneath it. This module is that layer: testable code owning the connection and query logic so the interface 
stays focused on presentation.
## Getting Started
You will need MongoDB running locally with the AAC dataset loaded (aac.animals) and a readWrite user.
1. Keep CRUD_Python_Module.py alongside the script or notebook that imports it.
2. Confirm MongoDB is reachable at localhost:27017, or edit the HOST/PORT constants.
3. Instantiate the class with credentials: shelter = AnimalShelter("aacuser", "<password>").
## Installation
**PyMongo** - the officially supported MongoDB driver for Python; insert_one()/find() map directly onto create/read. pip install pymongo.

**MongoDB Community Server** - Austin Animal Center records aren't perfectly uniform, so a document database fit better than a rigid schema. mongoimport/mongosh loaded the dataset and created aacuser in Module Three.

**Jupyter Notebook** - let me re-run create()/read() calls against the live database while testing.
## Usage
##### Code Example
The class only needs a username and password; the database (aac) and collection (animals) are handled internally:

```
shelter = AnimalShelter("aacuser", "<password>")
shelter.create({"animal_id": "TEST1001", "breed": "Labrador Retriever Mix",
  "animal_type": "Dog", "outcome_type": "Adoption"})   # -> True
results = shelter.read({"animal_type": "Dog"})
len(results)                                            # -> 5593
```

`create()` checks it received a non-empty dict before touching the database, then returns result.acknowledged rather than assuming success just
because `insert_one()` did not raise. `read()` calls `find()`, not `find_one()`, wrapping the cursor in `list()` so multi-document matches are not silently 
dropped.
##### Tests
Both methods were tested against the live aac database in ModuleFourTestScript.ipynb, not mocked. `create()` returned True, and the document was findable
right away by its `animal_id`. One real snag: re-running that cell inserted a fresh document each time, since `animal_id` isn't enforced as unique, so the
query eventually matched four documents, a good argument for a unique index in Project One. A wider `read()` for every Dog record returned 5,593 documents.
##### Screenshots
<img width="975" height="819" alt="image" src="https://github.com/user-attachments/assets/e6e86869-194b-48fe-b485-4b3680acc9bc" />

Connected -- shelter object is ready.
```
Insert succeeded: True   |   Documents found: 4   |   Dog records found: 5593
```
## Contact
Sean Singh
