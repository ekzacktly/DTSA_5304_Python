from pulp import *
mdl = LpProblem('my_problem', LpMaximize)
x = LpVariable('x', lowBound = 0)
y = LpVariable('y', lowBound = 0, upBound = 4)
mdl += (x + 2 * y)
mdl += x <= y + 3
mdl += x >= y - 1
mdl += x - 2 * y <= 5
print(y.value())
status= mdl.solve()
print(x.value())
print(y.value())
print(mdl.objective.value())


from pulp import *
mdl = LpProblem('n_problem', LpMaximize)
n = 15
vars = [ LpVariable(f'x{i}', lowBound = 0.0) for i in range(n)]
mdl += lpSum(vars)
for i in range(14):
    mdl += vars[i] - vars[i+1] <= i
    mdl += vars[i] - vars[i+1] >= -i
status = mdl.solve()
if status == LpStatusOptimal:
    print('Optimal solution found!')
    print([vi.value() for vi in vars])
    print(mdl.objective.value())
elif status == LpStatusInfeasible:
    print('Infeasible problem')
elif status == LpStatusUnbounded:
    print('Unbounded problem')
else:
    print('Unknown status')