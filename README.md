# Allelia

Allelia is a lightweight genetics library for games and simulations.

It allows you to define genes and alleles, create parent genomes, and generate child genetics using direct inheritance, blending, and mutation.

Allelia is designed to be flexible rather than biologically accurate. The library handles the inheritance system while your game or simulation determines what the genetic information represents.

## Features

- Continuous genes
- Discrete genes
- Direct inheritance
- Blended inheritance
- Mutation
- Genotypes and phenotypes
- Custom inheritance functions
- Custom expression functions
- Custom mutation functions
- One or more parents
- Numeric, tuple, list, and dictionary blending

## Basic Concepts

### Gene

A `Gene` defines how a particular genetic trait behaves.

```python
from allelia import Gene

eye_color = Gene(
	"eye_color",
	"continuous"
)
```

Allelia currently supports two gene types:

```python
"continuous"
"discrete"
```

Continuous genes can blend their alleles together.

Discrete genes select individual alleles without blending them.

---

### Genome

A `Genome` stores the alleles belonging to an individual.

```python
from allelia import Genome

parent = Genome()

parent.set(
	"eye_color",
	[
		(110, 70, 40),
		(70, 130, 180)
	]
)
```

You can retrieve the genotype with:

```python
parent.get(
	"eye_color"
)
```

You can also check whether a genome contains a gene:

```python
parent.has(
	"eye_color"
)
```

---

## Creating an Allelia System

Create an `Allelia` instance and register the genes used by your system.

```python
from allelia import Allelia, Gene

allelia = Allelia()

allelia.add_gene(
	Gene(
		"eye_color",
		"continuous"
	)
)
```

By default, inheritance probabilities are:

```text
Direct Inheritance: 80%
Blending:           18%
Mutation:            2%
```

You can change these when creating the system:

```python
allelia = Allelia(
	direct_inheritance=0.80,
	blending=0.18,
	mutation=0.02
)
```

The values are treated as relative weights, so they do not have to add up to exactly `1.0`.

---

# Creating Parents

Each parent is represented by a `Genome`.

```python
parent_1 = Genome()

parent_1.set(
	"eye_color",
	[
		(110, 70, 40),
		(70, 130, 180)
	]
)


parent_2 = Genome()

parent_2.set(
	"eye_color",
	[
		(80, 130, 75),
		(130, 145, 150)
	]
)
```

In this example, each parent has two eye color alleles.

---

# Creating a Child

Pass the parent genomes to:

```python
allelia.create_child()
```

For example:

```python
child = allelia.create_child(
	parent_1,
	parent_2
)
```

Each parent contributes one allele for every gene that parent contains.

The resulting child stores those contributions as its genotype.

```python
print(
	child.get("eye_color")
)
```

---

# Phenotypes

A genotype contains an individual's alleles.

A phenotype is the allele that is expressed.

Use:

```python
allelia.express()
```

to generate a phenotype from a genome.

```python
child_phenotype = allelia.express(
	child
)

print(
	child_phenotype["eye_color"]
)
```

By default, Allelia randomly selects an allele from the genotype for expression.

Custom expression rules can also be supplied to a gene.

---

# Continuous Genes

Continuous genes allow values to be blended.

For example:

```python
Gene(
	"height",
	"continuous"
)
```

Allelia can blend numerical alleles:

```python
170
190
```

into an intermediate value.

Continuous genes can also contain more complicated numerical structures.

For example, RGB colors:

```python
[
	(110, 70, 40),
	(70, 130, 180)
]
```

can produce intermediate colors.

---

# Discrete Genes

Discrete genes represent traits that should remain separate rather than being mathematically blended.

For example:

```python
allelia.add_gene(
	Gene(
		"ear_type",
		"discrete"
	)
)
```

A genome might contain:

```python
parent.set(
	"ear_type",
	[
		"round",
		"pointed"
	]
)
```

Allelia selects one of the available alleles when that parent contributes the gene.

---

# Blending

Allelia includes a recursive `blend()` function.

It can blend:

- Numbers
- Tuples
- Lists
- Dictionaries

For example:

```python
from allelia.allelia import blend

result = blend(
	100,
	200,
	0.5
)

print(result)
```

Result:

```text
150.0
```

The ratio determines how much each value contributes.

```python
blend(
	100,
	200,
	0.25
)
```

uses:

```text
75% of the first value
25% of the second value
```

The same system works recursively with tuples:

```python
blend(
	(100, 50),
	(200, 100),
	0.5
)
```

and dictionaries:

```python
blend(
	{
		"x": 100,
		"y": 50
	},
	{
		"x": 200,
		"y": 100
	},
	0.5
)
```

This makes continuous genes useful for more than simple numbers.

---

# Mutation

Mutation behavior can be defined separately for each gene.

Create a function that accepts:

```python
allele
gene
```

For example:

```python
import random


def mutate_color(
	allele,
	gene
):
	return tuple(
		max(
			0,
			min(
				255,
				value + random.randint(-20, 20)
			)
		)
		for value in allele
	)
```

Then assign it to the gene:

```python
allelia.add_gene(
	Gene(
		"eye_color",
		"continuous",
		mutate=mutate_color
	)
)
```

When mutation is selected during inheritance, Allelia generates the inherited allele and passes it to your mutation function.

If no mutation function is supplied, the allele is returned unchanged.

This allows the application using Allelia to determine what mutation means for its particular data.

---

# Custom Expression

You can override the default phenotype behavior.

An expression function receives:

```python
genotype
gene
```

Example:

```python
def express_first(
	genotype,
	gene
):
	return genotype[0]
```

Then:

```python
Gene(
	"eye_color",
	"continuous",
	express=express_first
)
```

Allelia will use your function instead of randomly selecting an allele.

---

# Custom Inheritance

Genes can also provide their own inheritance behavior.

An inheritance function receives:

```python
genotype
gene
```

For example:

```python
def inherit_first(
	genotype,
	gene
):
	return genotype[0]
```

Then:

```python
Gene(
	"special_gene",
	"continuous",
	inherit=inherit_first
)
```

This allows individual genes to override Allelia's default contribution behavior.

---

# More Than Two Parents

Allelia does not require exactly two parents.

`create_child()` accepts one or more parent genomes.

For example:

```python
child = allelia.create_child(
	parent_1,
	parent_2,
	parent_3
)
```

Each parent that contains a particular gene contributes one allele to the child's genotype for that gene.

This allows Allelia to support fictional reproductive systems without requiring special handling inside the library.

---

# Complete Example

```python
from allelia import Allelia, Gene, Genome


allelia = Allelia()


allelia.add_gene(
	Gene(
		"eye_color",
		"continuous"
	)
)


parent_1 = Genome()

parent_1.set(
	"eye_color",
	[
		(110, 70, 40),
		(70, 130, 180)
	]
)


parent_2 = Genome()

parent_2.set(
	"eye_color",
	[
		(80, 130, 75),
		(130, 145, 150)
	]
)


child = allelia.create_child(
	parent_1,
	parent_2
)


phenotype = allelia.express(
	child
)


print(
	"Parent 1:",
	parent_1.get("eye_color")
)

print(
	"Parent 2:",
	parent_2.get("eye_color")
)

print(
	"Child:",
	child.get("eye_color")
)

print(
	"Expressed Color:",
	phenotype["eye_color"]
)
```

Running the example multiple times can produce different results because inheritance, blending ratios, mutation, and phenotype expression can use randomness.

---

# Design Philosophy

Allelia separates genetic rules from the meaning of the data.

The library does not need to know that:

```python
(70, 130, 180)
```

represents an eye color or that:

```python
(120, 80)
```

represents a point in a procedural character model.

To Allelia, they are simply alleles.

This allows the same inheritance system to be used for character appearance, creature generation, fictional species, procedural traits, or other game and simulation systems.

Applications remain responsible for deciding what their genes represent and how their resulting phenotypes are used.

---

# Version

Current version:

```text
0.1.0
```

Allelia is currently an early-stage library. The API may change as the library is expanded and tested in additional projects.
