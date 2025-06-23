from flask import Flask, render_template, request
import math

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        expr = request.form['expression']
        result = eval_expr(expr)
        return render_template('index.html', result=result, expression=expr)
    except Exception as e:
        return render_template('index.html', result="Error", expression="")

# Safe eval with math functions and constants, using degrees for trig functions
def eval_expr(expr):
    allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
    # Override trig functions to use degrees
    allowed_names['sin'] = lambda x: math.sin(math.radians(x))
    allowed_names['cos'] = lambda x: math.cos(math.radians(x))
    allowed_names['tan'] = lambda x: math.tan(math.radians(x))
    allowed_names['abs'] = abs
    allowed_names['pi'] = math.pi
    allowed_names['sqrt'] = math.sqrt
    allowed_names['log'] = math.log
    allowed_names['exp'] = math.exp

    code = compile(expr, "<string>", "eval")
    for name in code.co_names:
        if name not in allowed_names:
            raise NameError(f"Use of '{name}' not allowed")
    return eval(code, {"__builtins__": {}}, allowed_names)

if __name__ == '__main__':
    app.run(debug=True)
