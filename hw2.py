class HTML:
	def __init__(self, **kwargs):
		self.tag = "html"     
		self.children = []

		for attr, value in kwargs.items():
			self.output = value

	def __iadd__(self, other):
		self.children.append(other)
		return self

	def __enter__(self):
		return self

	def __exit__(self, *args, **kwargs):
		# По умолчанию вывод в файл, для вывода в консоль в строке 137 изменить значение output=None
		if self.output is not None:
			with open("test.html", "w") as file:
				file.write(str(self))
		else:
			print("<%s>" % self.tag)
			for child in self.children:
				print(str(child))
			print("</%s>" % self.tag)


	def __str__(self):
		line = "<{tag}>\n".format(tag=self.tag)
		for child in self.children:
			line += str(child)
		line += "\n</{tag}>".format(tag=self.tag)
		return line

class TopLevelTag:
	def __init__(self, tag, klass=None, **kwargs):
		self.tag = tag
		self.children = []
		self.attributes = {}

		# добавление классов в словарь атрибутов
		if klass is not None:
			self.attributes["class"] = " ".join(klass)

		#изменение форматирования атрибутов
		for attr, value in kwargs.items():
			if "_" in attr:
				attr = attr.replace("_", "-")
			self.attributes[attr] = value 

	def __iadd__(self, other):
		self.children.append(other)
		return self

	def __enter__(self):
		return self

	def __exit__(self, *args, **kwargs):
		pass

	def __str__(self):
		attrs = []
		for attribute, value in self.attributes.items():
			attrs.append('%s="%s"' % (attribute, value))
		attrs = " ".join(attrs)

		if len(self.attributes) != 0:
			opening = "<{tag} {attrs}>\n".format(tag=self.tag, attrs=attrs)
		else:
			opening = "<{tag}>\n".format(tag=self.tag)
		internal = ""
		for child in self.children:
			internal += str(child)
		ending = "\n</%s>" % self.tag
		return opening + internal + ending

class Tag:
	def __init__(self, tag, toplevel=False, is_single=False, klass=None, **kwargs):
		self.tag = tag
		self.text = ""
		self.attributes = {}
		self.toplevel = toplevel       
		self.is_single = is_single
		self.children = []

		if klass is not None:
			self.attributes["class"] = " ".join(klass)

		for attr, value in kwargs.items():
			if "_" in attr:
				attr = attr.replace("_", "-")
			self.attributes[attr] = value 

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		if self.toplevel:
			print("<%s>" % self.tag)
			for child in self.children:
				print(child)
			print("</%s>" % self.children)

	def __iadd__(self, other):
		self.children.append(other)
		return self

	def __str__(self):
		attrs = []
		for attribute, value in self.attributes.items():
			attrs.append('%s="%s"' % (attribute, value))
		attrs = " ".join(attrs)

		# При наличии вложенных тегов:
		if self.children:
			if len(self.attributes) != 0:
				opening = "\n<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
			else:
				opening = "\n<{tag}>".format(tag=self.tag)
			internal = "%s" % self.text
			for child in self.children:
				internal += "\n" + str(child)
			ending = "</%s>" % self.tag
			return opening + internal + ending
		else:
			# для непарного тега
			if self.is_single:
				return "<{tag} {attrs}/>\n".format(tag=self.tag, attrs=attrs)
			else:
				if len(self.attributes) != 0:
					return "<{tag} {attrs}>{text}</{tag}>".format(tag=self.tag, attrs=attrs, text=self.text)
				else:
					return "<{tag}>{text}</{tag}>".format(tag=self.tag, text=self.text)


if __name__ == "__main__":
	with HTML(output="test.html") as doc:
	    with TopLevelTag("head") as head:
	        with Tag("title") as title:
	            title.text = "hello"
	            head += title
	        doc += head

	    with TopLevelTag("body") as body:
	        with Tag("h1", klass=("main-text",)) as h1:
	            h1.text = "Test"
	            body += h1

	        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
	            with Tag("p") as paragraph:
	                paragraph.text = "another test"
	                div += paragraph

	            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
	                div += img

	            body += div

	        doc += body
