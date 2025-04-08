from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract
from datetime import datetime
import calendar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///matriz_indicadores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave_secreta_asd'

db = SQLAlchemy(app)

# Importar modelos
from models import Proceso, Indicador, Meta, Valor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/matriz')
def matriz():
    anio = request.args.get('anio', datetime.now().year, type=int)
    procesos = Proceso.query.all()
    
    # Diccionario para almacenar datos por proceso e indicador
    data = {}
    for proceso in procesos:
        data[proceso.id] = {
            'nombre': proceso.nombre,
            'indicadores': {}
        }
        for indicador in proceso.indicadores:
            data[proceso.id]['indicadores'][indicador.id] = {
                'nombre': indicador.nombre,
                'metas': {},
                'valores': {},
                'calificaciones': {}
            }
            # Obtener metas del año seleccionado
            metas = Meta.query.filter_by(indicador_id=indicador.id, anio=anio).all()
            for meta in metas:
                data[proceso.id]['indicadores'][indicador.id]['metas'][meta.mes] = meta.valor
            
            # Obtener valores reales del año seleccionado
            valores = Valor.query.filter_by(indicador_id=indicador.id, anio=anio).all()
            for valor in valores:
                data[proceso.id]['indicadores'][indicador.id]['valores'][valor.mes] = valor.valor
                data[proceso.id]['indicadores'][indicador.id]['calificaciones'][valor.mes] = valor.calificacion
    
    # Obtener meses (1-12)
    meses = list(range(1, 13))
    nombres_meses = [calendar.month_name[mes] for mes in meses]
    
    return render_template('matriz.html', data=data, anio=anio, meses=meses, 
                          nombres_meses=nombres_meses, procesos=procesos)

@app.route('/charts')
def charts():
    anio = request.args.get('anio', datetime.now().year, type=int)
    return render_template('charts.html', anio=anio)

@app.route('/api/chart_data/<int:indicador_id>/<int:anio>')
def chart_data(indicador_id, anio):
    indicador = Indicador.query.get_or_404(indicador_id)
    
    # Obtener datos para el gráfico
    metas = Meta.query.filter_by(indicador_id=indicador_id, anio=anio).all()
    valores = Valor.query.filter_by(indicador_id=indicador_id, anio=anio).all()
    
    # Crear listas para los datos
    meses = list(range(1, 13))
    nombres_meses = [calendar.month_name[mes] for mes in meses]
    datos_meta = [None] * 12
    datos_valor = [None] * 12
    
    # Asignar valores a las listas
    for meta in metas:
        datos_meta[meta.mes - 1] = meta.valor
    
    for valor in valores:
        datos_valor[valor.mes - 1] = valor.valor
    
    # Calcular promedio YTD para meta y valor
    metas_validas = [m for m in datos_meta if m is not None]
    valores_validos = [v for v in datos_valor if v is not None]
    
    promedio_meta = sum(metas_validas) / len(metas_validas) if metas_validas else None
    promedio_valor = sum(valores_validos) / len(valores_validos) if valores_validos else None
    
    # Añadir el YTD al final
    nombres_meses.append('YTD')
    datos_meta.append(promedio_meta)
    datos_valor.append(promedio_valor)
    
    return jsonify({
        'nombre_indicador': indicador.nombre,
        'labels': nombres_meses,
        'datasets': [
            {
                'label': 'Meta',
                'data': datos_meta,
                'borderColor': 'blue',
                'backgroundColor': 'transparent',
                'borderWidth': 2,
                'fill': false
            },
            {
                'label': 'Valor Real',
                'data': datos_valor,
                'borderColor': 'red',
                'backgroundColor': 'transparent',
                'borderWidth': 2,
                'fill': false
            }
        ]
    })

@app.route('/procesos')
def procesos_lista():
    procesos = Proceso.query.all()
    return render_template('procesos.html', procesos=procesos)

@app.route('/proceso/<int:proceso_id>')
def proceso_detalle(proceso_id):
    proceso = Proceso.query.get_or_404(proceso_id)
    return render_template('proceso_detalle.html', proceso=proceso)

@app.route('/indicadores')
def indicadores_lista():
    indicadores = Indicador.query.all()
    return render_template('indicadores.html', indicadores=indicadores)

@app.route('/indicador/<int:indicador_id>')
def indicador_detalle(indicador_id):
    indicador = Indicador.query.get_or_404(indicador_id)
    anio = request.args.get('anio', datetime.now().year, type=int)
    
    # Obtener metas y valores del indicador para el año seleccionado
    metas = Meta.query.filter_by(indicador_id=indicador_id, anio=anio).all()
    valores = Valor.query.filter_by(indicador_id=indicador_id, anio=anio).all()
    
    # Crear diccionarios para acceder fácilmente a los datos por mes
    metas_dict = {meta.mes: meta.valor for meta in metas}
    valores_dict = {valor.mes: valor.valor for valor in valores}
    calificaciones_dict = {valor.mes: valor.calificacion for valor in valores}
    
    # Obtener meses (1-12)
    meses = list(range(1, 13))
    nombres_meses = [calendar.month_name[mes] for mes in meses]
    
    return render_template('indicador_detalle.html', indicador=indicador, 
                          metas=metas_dict, valores=valores_dict, 
                          calificaciones=calificaciones_dict,
                          meses=meses, nombres_meses=nombres_meses, anio=anio)

@app.route('/indicador/nuevo', methods=['GET', 'POST'])
def indicador_nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form.get('descripcion', '')
        unidad = request.form['unidad']
        proceso_id = request.form['proceso_id']
        
        indicador = Indicador(
            nombre=nombre,
            descripcion=descripcion,
            unidad=unidad,
            proceso_id=proceso_id
        )
        
        db.session.add(indicador)
        db.session.commit()
        
        flash('Indicador creado exitosamente', 'success')
        return redirect(url_for('indicadores_lista'))
    
    procesos = Proceso.query.all()
    return render_template('indicador_form.html', procesos=procesos)

@app.route('/meta/nueva', methods=['GET', 'POST'])
def meta_nueva():
    if request.method == 'POST':
        valor = float(request.form['valor'])
        anio = int(request.form['anio'])
        mes = int(request.form['mes'])
        indicador_id = int(request.form['indicador_id'])
        
        # Verificar si ya existe una meta para este indicador, año y mes
        meta_existente = Meta.query.filter_by(
            indicador_id=indicador_id,
            anio=anio,
            mes=mes
        ).first()
        
        if meta_existente:
            meta_existente.valor = valor
            flash('Meta actualizada exitosamente', 'success')
        else:
            meta = Meta(
                valor=valor,
                anio=anio,
                mes=mes,
                indicador_id=indicador_id
            )
            db.session.add(meta)
            flash('Meta creada exitosamente', 'success')
        
        db.session.commit()
        return redirect(url_for('indicador_detalle', indicador_id=indicador_id, anio=anio))
    
    indicador_id = request.args.get('indicador_id', type=int)
    indicador = Indicador.query.get_or_404(indicador_id) if indicador_id else None
    anio = request.args.get('anio', datetime.now().year, type=int)
    mes = request.args.get('mes', 1, type=int)
    
    indicadores = Indicador.query.all() if not indicador else None
    
    return render_template('meta_form.html', indicador=indicador, 
                          indicadores=indicadores, anio=anio, mes=mes)

@app.route('/valor/nuevo', methods=['GET', 'POST'])
def valor_nuevo():
    if request.method == 'POST':
        valor = float(request.form['valor'])
        anio = int(request.form['anio'])
        mes = int(request.form['mes'])
        calificacion = float(request.form['calificacion']) if request.form['calificacion'] else None
        indicador_id = int(request.form['indicador_id'])
        
        # Verificar si ya existe un valor para este indicador, año y mes
        valor_existente = Valor.query.filter_by(
            indicador_id=indicador_id,
            anio=anio,
            mes=mes
        ).first()
        
        if valor_existente:
            valor_existente.valor = valor
            valor_existente.calificacion = calificacion
            flash('Valor actualizado exitosamente', 'success')
        else:
            nuevo_valor = Valor(
                valor=valor,
                anio=anio,
                mes=mes,
                calificacion=calificacion,
                indicador_id=indicador_id
            )
            db.session.add(nuevo_valor)
            flash('Valor creado exitosamente', 'success')
        
        db.session.commit()
        return redirect(url_for('indicador_detalle', indicador_id=indicador_id, anio=anio))
    
    indicador_id = request.args.get('indicador_id', type=int)
    indicador = Indicador.query.get_or_404(indicador_id) if indicador_id else None
    anio = request.args.get('anio', datetime.now().year, type=int)
    mes = request.args.get('mes', 1, type=int)
    
    indicadores = Indicador.query.all() if not indicador else None
    
    return render_template('valor_form.html', indicador=indicador, 
                          indicadores=indicadores, anio=anio, mes=mes)

if __name__ == '__main__':
    app.run(debug=True)