import random


class Gene:
	def __init__(
		self,
		name,
		gene_type,
		inherit=None,
		express=None,
		mutate=None
	):
		self.name = name
		self.gene_type = gene_type

		self.inherit_method = inherit
		self.express_method = express
		self.mutate_method = mutate

	def contribute(self, genotype):
		if self.inherit_method is not None:
			return self.inherit_method(
				genotype,
				self
			)

		if self.gene_type == "continuous":
			return self._inherit_continuous(
				genotype
			)

		if self.gene_type == "discrete":
			return self._inherit_discrete(
				genotype
			)

		raise ValueError(
			f"Unknown gene type: {self.gene_type}"
		)

	def express(self, genotype):
		if self.express_method is not None:
			return self.express_method(
				genotype,
				self
			)

		return random.choice(
			genotype
		)

	def mutate(self, allele):
		if self.mutate_method is not None:
			return self.mutate_method(
				allele,
				self
			)

		return allele

	def _inherit_continuous(self, genotype):
		if len(genotype) == 1:
			return genotype[0]

		allele_1 = random.choice(
			genotype
		)

		allele_2 = random.choice(
			genotype
		)

		ratio = random.random()

		return blend(
			allele_1,
			allele_2,
			ratio
		)

	def _inherit_discrete(self, genotype):
		return random.choice(
			genotype
		)


class Genome:
	def __init__(
		self,
		genes=None
	):
		if genes is None:
			genes = {}

		self.genes = genes

	def set(
		self,
		gene_name,
		alleles
	):
		self.genes[gene_name] = alleles

	def get(
		self,
		gene_name
	):
		return self.genes[gene_name]

	def has(
		self,
		gene_name
	):
		return gene_name in self.genes


class Allelia:
	def __init__(
		self,
		direct_inheritance=0.80,
		blending=0.18,
		mutation=0.02
	):
		self.genes = {}

		self.direct_inheritance = direct_inheritance
		self.blending = blending
		self.mutation = mutation

	def add_gene(
		self,
		gene
	):
		self.genes[gene.name] = gene

	def get_gene(
		self,
		gene_name
	):
		return self.genes[gene_name]

	def create_child(
		self,
		*parents
	):
		if len(parents) == 0:
			raise ValueError(
				"At least one parent is required."
			)

		child = Genome()

		for gene_name, gene in self.genes.items():
			child_alleles = []

			for parent in parents:
				if not parent.has(gene_name):
					continue

				parent_genotype = parent.get(
					gene_name
				)

				allele = self._inherit(
					gene,
					parent_genotype
				)

				child_alleles.append(
					allele
				)

			if child_alleles:
				child.set(
					gene_name,
					child_alleles
				)

		return child

	def express(
		self,
		genome
	):
		phenotype = {}

		for gene_name, gene in self.genes.items():
			if not genome.has(gene_name):
				continue

			genotype = genome.get(
				gene_name
			)

			phenotype[gene_name] = gene.express(
				genotype
			)

		return phenotype

	def _inherit(
		self,
		gene,
		genotype
	):
		inheritance_type = self._choose_inheritance_type()

		if inheritance_type == "direct":
			return random.choice(
				genotype
			)

		if inheritance_type == "blending":
			return gene.contribute(
				genotype
			)

		if inheritance_type == "mutation":
			allele = gene.contribute(
				genotype
			)

			return gene.mutate(
				allele
			)

	def _choose_inheritance_type(self):
		total = (
			self.direct_inheritance
			+ self.blending
			+ self.mutation
		)

		if total <= 0:
			raise ValueError(
				"Inheritance probabilities must total more than 0."
			)

		value = random.random() * total

		if value < self.direct_inheritance:
			return "direct"

		value -= self.direct_inheritance

		if value < self.blending:
			return "blending"

		return "mutation"


def blend(
	value_1,
	value_2,
	ratio=0.5
):
	if isinstance(
		value_1,
		(int, float)
	) and isinstance(
		value_2,
		(int, float)
	):
		return (
			value_1 * (1 - ratio)
			+ value_2 * ratio
		)

	if isinstance(
		value_1,
		tuple
	) and isinstance(
		value_2,
		tuple
	):
		return tuple(
			blend(
				a,
				b,
				ratio
			)
			for a, b in zip(
				value_1,
				value_2
			)
		)

	if isinstance(
		value_1,
		list
	) and isinstance(
		value_2,
		list
	):
		return [
			blend(
				a,
				b,
				ratio
			)
			for a, b in zip(
				value_1,
				value_2
			)
		]

	if isinstance(
		value_1,
		dict
	) and isinstance(
		value_2,
		dict
	):
		return {
			key: blend(
				value_1[key],
				value_2[key],
				ratio
			)
			for key in value_1
		}

	return random.choice(
		[
			value_1,
			value_2
		]
	)