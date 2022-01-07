# DE001 Standard error propagation model

## Scope

This document provides definition of the standard error propagation model, which is used for the calculation of the uncertainty of the values calculated from one or more measured values with the respective measurement error / uncertainty. This model is applied to the binary arithmetic operations between two measured values (with the uncertainties) as well as to the functions of one or more measured values.

## Background: Taylor series and linear approximation

The value of a function $f(x)$ in the vicinity of the point $x_0$ can be expressed in terms of Taylor series, as long as this function is infinitely differentiable at that point

$$f(x_0 + \Delta x) = f(x_0) + \sum_{n=1}^{\infty} {\frac{d^n f}{d x^n}(x_0) \times \frac{\Delta x^n}{n!}}$$

The linear approximation of the Taylor series expansion is limited to the first derivative, therefore, it is applicable to any function, which has, at least, the first derivative

$$\Delta f = f(x_0 + \Delta x) - f(x_0) \approx \frac{df}{dx}(x_0) \times \Delta x$$

The linear approximation can be extended to the functions of multiple variables using the partial derivatives

$$\begin{split}
\Delta f &= f(x_1 + \Delta x_1, x_2 + \Delta x_2, ..., x_N + \Delta x_N) - f(x_1, x_2, ..., x_N) \\
         &\approx \sum_{n=1}^{N}{\frac{\partial f}{\partial x_n}(x_1, x_2, ..., x_N) \times \Delta x_n}
\end{split}$$

## Model definition

Application of the function *f* on the values of a sample **X** of a random variable generates a set (sample) of values **Z**, which itself is a random variable

$$\mathbf{X} \xrightarrow{f} \mathbf{Z} : \mathbf{X} = \{ x_1, x_2, ..., x_N \}, \, \mathbf{Z} = \{ z_1, z_2, ..., z_N \} \equiv z_i = f(x_i) \, \forall \, i \in [1, N]$$

The values of the sample **X** can be also expressed in terms of displacement from (difference with) the sample's mean

$$\bar{x} = \frac{\sum_{i=1}^{N}{x_i}}{N} \Rightarrow  \Delta x_i = x_i - \bar{x} \, : \, \frac{\sum_{i=1}^{N}{\Delta x_i}}{N} = 0$$

Thus, the values of the **Z** random variable sample are expressed using linear approximation as

$$
\begin{split}
z_i & = f(x_i) \equiv f(\bar{x} + \Delta x_i) \approx f(\bar{x}) + \frac{df}{dx}(\bar{x}) \times \Delta x_i \\
    & \Rightarrow \bar{z} = \frac{\sum_{i=1}^{N}{z_i}}{N} \approx f(\bar{x})
\end{split}
$$

The variance of the **Z** sample is then approximated as

$$Var(z) = \frac{\sum_{i=1}^{N}{\left( z_i - \bar{z} \right)^2}}{N} \approx \left( \frac{df}{dx}(\bar{x})\right)^2 \times \frac{\sum_{i=1}^{N}{(\Delta x_i)^2}}{N} = \left( \frac{df}{dx}(\bar{x})\right)^2 \times Var(x)$$

In the case of the function of multiple variables the generated values **Z** form a random variable sample as well

$$
\begin{split}
\mathbf{X_1, X_2, ..., X_K} \xrightarrow{f} \mathbf{Z} : \mathbf{X_1} & = \{ x_{1,1}, x_{1,2}, ..., x_{1,N} \}, \\
                                                         \mathbf{X_2} & = \{ x_{2,1}, x_{2,2}, ..., x_{2,N} \}, \\
                                                                      & ... \\
                                                         \mathbf{X_K} & = \{ x_{K,1}, x_{K,2}, ..., x_{K,N} \}, \\
                                                         \mathbf{Z} & = \{ z_1, z_2, ..., z_N \} \\
                                                         \equiv z_i & = f(x_{1,i}, x_{2, i}, ..., x_{K,i}) \, \forall \, i \in [1, N]
\end{split}
$$

Thus, in the linear approximation

$$z_i \approx f(\bar{x}_1, \bar{x}_2, ..., \bar{x}_K) + \sum_{k=1}^{K}{\frac{\partial f}{\partial x_k}(\bar{x}_1, \bar{x}_2, ..., \bar{x}_K) \times \Delta x_{k,i}} \, : \, \Delta x_{k,i} = x_{k,i} - \bar{x}_k$$

where the *mean* values of each 'input' variable are calculated independently for each 'dimension'. Then, the variance of **Z** variable is approximated as

$$
\begin{split}
Var(z) & \approx \sum_{k=1}^{K}{\left( \frac{\partial f}{\partial x_k}(\bar{x}_1, \bar{x}_2, ..., \bar{x}_K) \right)^2 \times Var(x_k)} \\
       & + 2 \times \sum_{k=1}^{K-1}{\sum_{m=k+1}^{K}{\frac{\partial f}{\partial x_k}(\bar{x}_1, \bar{x}_2, ..., \bar{x}_K)} \times \frac{\partial f}{\partial x_m}(\bar{x}_1, \bar{x}_2, ..., \bar{x}_K) \times Cov(x_k, x_m)}
\end{split}
$$

The most common case is the function of two variables

$$\mathbf{X}, \mathbf{Y} \xrightarrow{f} \mathbf{Z} \equiv \mathbf{Z} = f(\mathbf{X}, \mathbf{Y}) \, : \, z_i = f(x_i, y_i) \, \forall \, i \in [1, N]$$

Therefore, the variance of **Z** is approximated

$$
\begin{split}
Var(z) & \approx \left( \frac{\partial f}{\partial x}(\bar{x},\bar{y})\right)^2 \times Var(x) + \left( \frac{\partial f}{\partial y}(\bar{x},\bar{y})\right)^2 \times Var(y) \\
       & + \frac{\partial f}{\partial x}(\bar{x},\bar{y}) \times \frac{\partial f}{\partial y}(\bar{x},\bar{y}) \times Cov(x,y)
\end{split}
$$

In the case of the the independent variables $Cov(x,y) = 0$, hence

$$Var(z) \approx \left( \frac{\partial f}{\partial x}(\bar{x},\bar{y})\right)^2 \times Var(x) + \left( \frac{\partial f}{\partial y}(\bar{x},\bar{y})\right)^2 \times Var(y)$$

Note that any binary arithmetic operation is a function of two variables, therefore this equation is also used for the derivation of the estimator of the standard error / uncertainty of the sum, difference, product and ratio of two measured values, as well as of the exponentiation. Note, that in the case of one operand being a constant (not measured value) the formula for a single argument function must be utilized.

Considering the *analogue measurements*, the half of the scale division is the estimator of the variance of the measured value with the repetitive readings on the same device, providing that the actual quantity being measured does not change between the takes. For the *digital measurements*, specifically based on the sampling of a detector, the standard error of the sample's mean is the variance of the measured value with the repetitive takes. So, the half scale division (for analogue) and standard error of the mean (for digital, sampled measurements) is the measurement uncertainty, which should be substituted for the variance(s) in the formulas above. The calculated *Var(z)* is the estimator of the uncertainty of the derived value.

Usually, each individual measured value involved in a calculation is considerd to be an indepenent variable, therefore the covariance term is exclude. Indeed, it is the case when two different quantities are measured (e.g. voltage and current to determine the resistance of or power dissipated by an electric component) or the same quantity but of the different objects or parts of the same object (e.g. width and length to determine the surface area, or lengths of the consequent cuts of a rope / plank to calculated the total length, etc.).

However, consider the following equivalences $2 \times x \equiv x + x$ or $x^2 \equiv x \times x$. The covariance term must be included in the formula for the 2-arguments function when the both arguments are identical (same variable / object in memory), where $Cov(x,x) \equiv Var(x)$ - otherwise the uncertainty estimators calculated using the left and right-side operations (effectively, formulas for 1 and 2 arguments functions) will produce the different results.
