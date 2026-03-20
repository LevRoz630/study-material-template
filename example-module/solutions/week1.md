# Week 1 Solutions

## Question 1

### (a) Show that \( W \) is a subspace of \( V \)

**Concept:** A subset \( W \subseteq V \) is a subspace if it is non-empty and closed under addition and scalar multiplication.

**Step 1:** \( \mathbf{0} = (0, 0, 0) \in W \) since \( 0 + 0 + 0 = 0 \). So \( W \neq \emptyset \).

**Step 2 (Closure under addition):** Let \( \mathbf{u} = (u_1, u_2, u_3), \mathbf{v} = (v_1, v_2, v_3) \in W \).
Then \( u_1 + u_2 + u_3 = 0 \) and \( v_1 + v_2 + v_3 = 0 \).
\[
\mathbf{u} + \mathbf{v} = (u_1 + v_1, u_2 + v_2, u_3 + v_3)
\]
Sum of components: \( (u_1 + v_1) + (u_2 + v_2) + (u_3 + v_3) = (u_1 + u_2 + u_3) + (v_1 + v_2 + v_3) = 0 + 0 = 0 \).
So \( \mathbf{u} + \mathbf{v} \in W \). ✓

**Step 3 (Closure under scalar multiplication):** Let \( \alpha \in \mathbb{R} \), \( \mathbf{u} \in W \).
\[
\alpha \mathbf{u} = (\alpha u_1, \alpha u_2, \alpha u_3)
\]
Sum: \( \alpha u_1 + \alpha u_2 + \alpha u_3 = \alpha(u_1 + u_2 + u_3) = \alpha \cdot 0 = 0 \).
So \( \alpha \mathbf{u} \in W \). ✓

Hence \( W \) is a subspace of \( V \). \( \square \)

### (b) Find a basis for \( W \)

\( W = \{(x, y, z) : x + y + z = 0\} \), so \( z = -x - y \).
General element: \( (x, y, -x-y) = x(1, 0, -1) + y(0, 1, -1) \).

$\boxed{\{(1, 0, -1), (0, 1, -1)\}}$ is a basis for \( W \).

### (c) Dimension

$\boxed{\dim(W) = 2}$
