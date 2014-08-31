# typing: Annotate Your Python Code

## What is typing?

Typing is intended as a standard notation for Python function and variable type annotations.
The notation can be used for documenting code in a concise, standard format, and it has been
designed to also be used by static and runtime type checkers, static analyzers, IDEs and other
tools. The typing module originates from the [mypy](http://www.mypy-lang.org/) optional static
type checker for Python.

Typing defines a notation and semantics for types. It does not define how to perform
type checking or type inference, and some details are left open, on purpose.
The typing module also includes some utilities that are primarily intended for type checkers
and static analyzers, and it contains some recommendations on how they should be used.

Typing has two implementations, one for Python 3.2+ and another for Python 2.7. Since
Python 2 does not support function annotations, another approach for encoding function
annotations must be used.

## Status

Typing is in development. Almost all design decisions are still open for discussion. Currently
we actively seek feedback from the community.

## Why a standard notation for types?

Annotating functions and modules is primarily useful for tools. Type checkers
and static analysis tools have a hard time unless
some form of description of the types of C extension modules is available. For example,
function return types cannot be easily inferred from C code. Also, inferring types
from Python programs
without annotations if tricky, and some annotations make type inference much more effective and
efficient.

Currently several ways of annotating types in Python code exist, none of which
are in widespread use. Some are based on docstrings, some
on function decorators, some on separate type definition files, and others on
Python 3 function annotations. This results in wasted, redundant effort
and fragmentation, and there is a risk that none of the approaches reach a critical mass needed
for wider adoption. By concentrating efforts on a single annotation syntax it's more likely
that type annotations would become genuinely useful for the community.

Type annotations will still be completely optional. It seems likely that the majority of Python
users would not feel the need to annote their code, and that's totally fine. However, even
they could benefit from a standard type annotation syntax, as tools such as IDEs and static
analyzers could become much more useful for users with unannoted code as well.

## Overview of the notation

### Concrete types

An annotation that is a reference to a type object such as `int` specifies a type that
is compatible with all instances of `int` and any subclasses of `int`. This is called
a *concrete type*. However, since Python uses duck typing, such annotation should
also accept any type sufficiently similar to `int` (see `@ducktype` below for how to
explicitly specify duck typing relationships).

User-defined classes and library types can also be used as concrete types.

Note that since `bool` is a subclass of `int`, `True` and `False` are compatible with
the type `int`.

### None

The `None` value can be used as a type. The only valid value is `None`. As a function return
type, it is used to specify that the function returns no useful value (i.e., it always returns
`None`).

### Tuple types

The type `typing.Tuple[t1, ... tN]` is a tuple type. It is a fixed-length, heterogeneous
`tuple` instance. Examples:

`Tuple[int, str]`

   This specifies a 2-tuple with `int` as the first item and `str` as the second item,
   such as `(1, 'x')`.

`Tuple[int]`

   This refers to a 1-tuple containing an integer, such as `(1,)`.

Note that there is no type for a zero-length tuple or an arbitrary-length tuple with uniform
types (though `Sequence[T]` can be used for the latter).

The concrete type `tuple` is compatible with arbitrary tuples, independent of lengths or item
types.

### Function types

The type `typing.Function[[A1, ...AN], R]` is a function (callable) type that is compatible
with any callable that can be called with positional arguments with types `A1`, ..., `AN`, and
that returns a value of type `R`.

There is no way of specifying types of functions taking an arbitrary number of arguments or
keyword-only arguments. This is a pretty rare use case, but falling back to `Any` (see below)
is always possible.

### The Any type

The type `typing.Any` is compatible with all values, and it is understood as a dynamically typed
value: there is an understanding that only some values are valid, but this is not specified
by the annotation. See also the type `object` below.

### The object type

The type `object` is a concrete type that is compatible with all values.
The intention is that a type `object`
signifies that an arbitrary object is valid (similar to type `Object` in Java), whereas `Any`
signifies that some constraints apply to the value, but these are either impossible to
represent using the annotation notation, or that the programmer has decided to not specify them.

### Union types

The type `typing.Union[T1, ..., TN]` is a type that is compatible with all item types
`T1`, ..., `TN`. The order of item types is arbitrary.

It may be tempting to use the union type `Union[int, float]`, but this is redundant, since
`int` is compatible with `float` (to see why, see `@ducktype` below) and thus this union
type is equivalent to just `float`.

### Type variables

Genericity or parametric polymorphism is supported via type variables. Type variable is
defined using `typing.typevar`; this is analogous to `namedtuple` in that the argument to
`typevar` should be the stringified name of the type variable:

```python
from typing import typevar
T = typevar('T')
```

A type variable can be conceptually instantiated with any type within the scope of a function
or a class (though the typing module does not actually perform this instantiation).
Consider this function (assuming the definition of `T` from above):

```python
def id(x: T) -> T:
    return x
```

`T` within the function can be replaced with any type. For example, if `T`, is replaced with
`int`, type type of the function becomes `int` -> `int`. The above annotation thus says
that `id` can be called with any argument type, and the return type is equivalent to the
argument type.

If the same type variable is used in multiple separate functions or classes, these instances of
`T` are independent of each other. References to a particular type variable within a single
function or class are always varied in a lockstep fashion.

### Type variable with value restriction

It is possible to define a type variable with a fixed set of valid values, using a `values`
keyword argument of `typevar`. The value of the keyword argument should be tuple literal:

```python
from typing import typevar

T = typevar('T', values=(str, bytes))

def f(s: T) -> T:
    return s[0] + t[-1]
```

Now `f` can be called with a `str` or `bytes` argument, and the return type is `str` or
`bytes`, respectively.

A type variable that ranges over `str` and `bytes` is often useful. Typing includes a
predefined type variable exactly like that, `AnyStr` (in Python 2 it ranges over `str` and
`unicode`). The above function `f` could
be equivalently written using `AnyStr`:

```python
from typing import AnyStr

def f(s: AnyStr) -> AnyStr:
    return s[0] + t[-1]
```

Union types and type variables with value restrictions are related but different. A type
variable is
always instantiated to a single value in lockstep fashion within the scope of the variable,
whereas each instance of a union type is independent of each other.

### Generic classes

A class can be generic, i.e. it is parametrized with one or more type arguments. A concrete
generic class extends the `typing.Generic` class:

```python
from typing import typevar, Generic

T = typevar('T')
S = typevar('S')

class G(Generic[T, S]):
    ...
```

The type variables `T` and `S` can be used in the body of `G`. Now `G` can be used as a
generic type using indexing, for example `G[int, str]`.

If the type arguments are omitted *within an annotation* (just `G`), the type variables will have
implicit `Any` values. The type `G` is thus equivalent to `G[Any, Any]`. However, if `G`
is used in an expression context, not using the indexing notation means that the type
arguments should be inferred from the context (but how this is achieved is out of the scope
of the typing module).

The indexing notation can also be used within expressions:

```python
g1 = G[int, str]()    # OK, explicit type arguments
g2 = G()              # OK, infer type arguments
```

Instances of a generic class don't keep track of the type arguments at runtime (i.e., they
are erased). This means that generic instances have no space overhead compared to normal class
instances.

*TODO: generic inheritance, abstract generic classes*

### Generic type aliases

The module `typing` defines several aliases for built-in types that allow using the generic
type syntax:

* `List[T]`: concrete `list` object with items of type `T`
* `Dict[K, V]`: concrete `dict` object with keys of type `K` and values of type `V`
* `Set[T]`: concrete `set` object with items of type `T`
* `Pattern[AnyStr]`: compiled regular expression
* `Match[AnyStr]`: regular expression match object

These aliases are needed since the built-in types do not support indexing. Similar to normal
generic classes, they can also be used in an expression context.

### Built-in generic ABCs

The typing module defines several generic variants of classes defined in `abc.collections`:

 * `Iterable[T]`
 * `Iterator[T]`
 * `Sequence[T]`
 * `Mapping[T]`
 * `AbstractSet[T]`

It also defines some additional ABCs:

 * `IO[AnyStr]` (file-like object)

*TODO: Describe additional generic ABCs.*

### String escapes

A type can be escaped as a string literal. For example, `"int"` should be equivalent to `int`.
This makes it possible to refer to types before they are defined (forward references).

### Variable annotations

Python has no syntax for variable annotations, but variable annotations are often useful.
Typing defines a helper class `Undefined` for this purpose. Initializing a variable
with `Undefined` can be used to declare the type of a variable:

```
from typing import Undefined, List
x = Undefined(List[int])
```

Now the type of `x` is declared as `List[int]`. An `Undefined` value should not be used at
runtime. Any operation on `x` above would raise an exception. However, passing an `Undefined`
value around
is valid, and Python considers `x` to be defined name. Thus a variable with an `Undefined` value
is different from an undefined name.

## Additional features

### Type casts

`cast(type, x)`

This is a no-op function that returns the second argument. It can be used by programmers
to tell tools that an expression should be understood to have a given type.

### Function overloading

*TODO: Describe*

### Ducktype compatibility

The `ducktype(t)` class decorator can be used to declare the target class to be *duck type
compatible*
with `t`. The details of what this means are left to be defined by individual tools, but
generally the intention is that a type that is duck type compatible with another type should
mean roughly that instances of the decorared class and any subclasses are compatible with the type
`t`.

For example, the `int` class should be duck type compatible with `float`, since `int` objects
are implicitly valid when `float`s are expected. Also, `float` should be duck type compatible
with `complex`.

*TODO: Add more examples*

## Details left unspecified

The semantics of several possible programs behaviors are left undefined. These are out
of the scope of this specification:

 * The concept of type compatibility (or subtyping) is intentionally left vague. Exact rules for
   subtyping, type equivalency, etc. are left to be defined by individual tools.
 * Typing does not specify how tools should behave if annotations are manipulated at runtime.
   They are free to ignore such modifications.
 * Typing does not specify how tools should behave if names of types or utility functions are
   modified at runtime. For example, if the `int` builtin is replaced with `float` at runtime,
   a tool can validly interpret references to `int` to still refer to integers, even the runtime
   value of the annotation can be `float`. Also, if the `typing.List` alias is redefined to
   point to `typing.Set`, tools can still understand a `List` type to refer to a list rather than
   a set.
 * Implementations can use arbitrary additional criteria to decide whether two types are duck type
   compatible. However, an implementation should honor `@ducktype` declarations.
 * Using a string literal annotation may make it impossible to determine the semantic value of the
   annotation at runtime. A tool
   is free to ignore or reject some or all string literal types.
