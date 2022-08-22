from ast import Not
from flask import Flask
from flask import render_template,request,redirect,flash,url_for
from flaskext.mysql import MySQL 
app = Flask(__name__)
app.secret_key="sena"

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema'

mysql.init_app(app)

@app.route('/')
def home():
    return render_template('jugador/home.html')

@app.route('/index.html')
def index():
    sql = "SELECT * FROM  `empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()
    
    conn.commit()
    
    return render_template('jugador/index.html', empleados=empleados)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM empleados WHERE id=%s",(id))
    conn.commit()
    return redirect('/index.html')

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empleados WHERE id=%s",(id))
    empleados = cursor.fetchall()
    conn.commit()
    return render_template('jugador/edit.html',empleados=empleados)

@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtnombre']
    _cedula=request.form['txtcedula']
    _edad=request.form['txtedad']
    id=request.form['txtid']
    
    if _nombre=='' or _cedula=='' or _edad=='':
        flash('debes llenar los datos de los campos')
        return redirect(url_for('index'))
    
    if not _cedula.isdigit() or not _edad.isdigit():
        flash('debes ingresar solo numeros en la cedula y la edad')
        return redirect(url_for('index'))
    
    if _nombre.isdigit():
        flash('debes ingresar solo letras en el nombre')
        return redirect(url_for('index'))
    
    if len(_cedula)>10:
        flash('debes ingresar solo 10 digitos maximo')
        return redirect(url_for('index'))
    
    if len(_edad)>3:
        flash('debes ingresar solo 3 digitos maximo')
        return redirect(url_for('index'))
    
   
    
    
    
    sql = "UPDATE empleados SET nombre=%s, cedula=%s, edad=%s WHERE id=%s ;"
    datos = (_nombre,_cedula,_edad,id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/index.html')

@app.route('/create')
def create():
    return render_template('jugador/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtnombre']
    _cedula=request.form['txtcedula']
    _edad=request.form['txtedad']
    
    if _nombre=='' or _cedula=='' or _edad=='':
        flash('debes llenar los datos de los campos')
        return redirect(url_for('create'))
    
    if not _cedula.isdigit() or not _edad.isdigit():
        flash('debes ingresar solo numeros en la cedula y la edad')
        return redirect(url_for('create'))
    
    if _nombre.isdigit():
        flash('debes ingresar solo letras en el nombre')
        return redirect(url_for('create'))
    
    if len(_cedula)>10:
        flash('debes ingresar solo 10 digitos maximo')
        return redirect(url_for('create'))
    
    if len(_edad)>3:
        flash('debes ingresar solo 3 digitos maximo')
        return redirect(url_for('create'))
    
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `cedula`, `edad`) VALUES (NULL, %s, %s,%s);"
    datos = (_nombre,_cedula,_edad)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/index.html')

#-----------------------torneos backend--------------------------------------------------------

@app.route('/indextorneo.html')
def indextorneo():
    sql = "SELECT * FROM  `torneos`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    torneos = cursor.fetchall()
    
    conn.commit()
    
    return render_template('torneos/indextorneo.html', torneos=torneos)

@app.route('/destroytorneo/<int:id>')
def destroytorneo(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM torneos WHERE id=%s",(id))
    conn.commit()
    return redirect('/indextorneo.html')

@app.route('/edittorneo/<int:id>')
def edittorneo(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM torneos WHERE id=%s",(id))
    torneos = cursor.fetchall()
    conn.commit()
    return render_template('torneos/edittorneo.html',torneos=torneos)

@app.route('/updatetorneo', methods=['POST'])
def updatetorneo():
    _nom_torneo=request.form['txtnom_torneo']
    _lugar=request.form['txtlugar']
    _esenario_depor=request.form['txtesenario_depor']
    _nom_organizador=request.form['txtnom_organizador']
    _tel_organizador=request.form['txttel_organizador']
    _fecha_ini=request.form['txtfecha_ini']
    _fecha_fin=request.form['txtfecha_fin']
    _deporte=request.form['txtdeporte']
    id=request.form['txtid']
    
    if _fecha_ini > _fecha_fin:
        flash('la fecha de finalizacion debe ser posterior a la fecha de inicio')
        return redirect(url_for('indextorneo'))
    
    if not _tel_organizador.isdigit():
        flash('debes ingresar solo numeros en la cedula y la edad')
        return redirect(url_for('indextorneo'))
    
    if _nom_torneo.isdigit() or _lugar.isdigit() or _esenario_depor.isdigit() or _nom_organizador.isdigit() or _deporte.isdigit():
        flash('debes ingresar solo letras en todos los campos exepto en telefono')
        return redirect(url_for('indextorneo'))
    
    sql = "UPDATE torneos SET nom_torneo=%s, lugar=%s, esenario_depor=%s, nom_organizador=%s, tel_organizador=%s, fecha_ini=%s, fecha_fin=%s, deporte=%s WHERE id=%s ;"
    datostor = (_nom_torneo,_lugar,_esenario_depor,_nom_organizador,_tel_organizador,_fecha_ini,_fecha_fin,_deporte,id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datostor)
    conn.commit()
    return redirect('/indextorneo.html')

@app.route('/createtorneo')
def createtorneo():
    return render_template('torneos/createtorneo.html')

@app.route('/storetorneo', methods=['POST'])
def storagetorneo():
    _nom_torneo=request.form['txtnom_torneo']
    _lugar=request.form['txtlugar']
    _esenario_depor=request.form['txtesenario_depor']
    _nom_organizador=request.form['txtnom_organizador']
    _tel_organizador=request.form['txttel_organizador']
    _fecha_ini=request.form['txtfecha_ini']
    _fecha_fin=request.form['txtfecha_fin']
    _deporte=request.form['txtdeporte']
    
    if not _tel_organizador.isdigit():
        flash('debes ingresar solo numeros en la cedula y la edad')
        return redirect(url_for('createtorneo'))
    
    if _nom_torneo.isdigit() or _lugar.isdigit() or _esenario_depor.isdigit() or _nom_organizador.isdigit() or _deporte.isdigit():
        flash('debes ingresar solo letras en todos los campos excepto en telefono')
        return redirect(url_for('createtorneo'))
    
    if _fecha_ini > _fecha_fin:
        flash('la fecha de finalizacion debe ser posterior a la fecha de inicio')
        return redirect(url_for('createtorneo'))
    
    sql = "INSERT INTO `torneos` (`nom_torneo`, `lugar`, `esenario_depor`, `nom_organizador`,`tel_organizador`,`fecha_ini`,`fecha_fin`,`deporte`,`id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NULL);"
    datostor = (_nom_torneo,_lugar,_esenario_depor,_nom_organizador,_tel_organizador,_fecha_ini,_fecha_fin,_deporte)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datostor)
    conn.commit()
    return redirect('/indextorneo.html')


if __name__ == '__main__':
    app.run(debug=True)

