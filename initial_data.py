from app import app, db, Proceso, Indicador, Meta, Valor

def poblar_datos_iniciales():
    with app.app_context():
        # Crear procesos
        procesos = [
            {'id': 1, 'nombre': 'Administracion', 'descripcion': 'Proceso de administración y gestión'},
            {'id': 2, 'nombre': 'Calidad', 'descripcion': 'Proceso de control de calidad'},
            {'id': 3, 'nombre': 'Finanzas', 'descripcion': 'Proceso financiero'},
            {'id': 4, 'nombre': 'Gestión Humana', 'descripcion': 'Proceso de recursos humanos'},
            {'id': 5, 'nombre': 'Logística', 'descripcion': 'Proceso de logística'},
            {'id': 6, 'nombre': 'Mantenimiento', 'descripcion': 'Proceso de mantenimiento'},
            {'id': 7, 'nombre': 'Planificación', 'descripcion': 'Proceso de planificación'},
            {'id': 8, 'nombre': 'Producción', 'descripcion': 'Proceso de producción'},
            {'id': 9, 'nombre': 'Ventas', 'descripcion': 'Proceso de ventas'},
            {'id': 10, 'nombre': 'Compras', 'descripcion': 'Proceso de compras'},
            {'id': 11, 'nombre': 'Operaciones', 'descripcion': 'Proceso de operaciones'},
        ]
        
        for p in procesos:
            proceso = Proceso(id=p['id'], nombre=p['nombre'], descripcion=p['descripcion'])
            db.session.add(proceso)
        
        # Comprometer los cambios para que los procesos estén disponibles
        db.session.commit()
        
        # Crear indicadores (ejemplo parcial)
        indicadores = [
            # Administración
            {'id': 1, 'nombre': 'Indice de Cumplimiento Estrategico (ICE)', 'unidad': '%', 'proceso_id': 1},
            
            # Calidad
            {'id': 2, 'nombre': 'Quejas de Clientes relacionadas a Calidad', 'unidad': 'cantidad', 'proceso_id': 2},
            {'id': 3, 'nombre': 'Hit Microbiológico', 'unidad': 'bool', 'proceso_id': 2},
            {'id': 4, 'nombre': 'Coliformes totales ≤ 10,000 UFC', 'unidad': 'UFC', 'proceso_id': 2},
            
            # Finanzas
            {'id': 5, 'nombre': 'Margen bruto en mix', 'unidad': '%', 'proceso_id': 3},
            {'id': 6, 'nombre': 'Ejecucion presupuestaria', 'unidad': '%', 'proceso_id': 3},
            {'id': 7, 'nombre': 'Costo de empaque por libra', 'unidad': '%', 'proceso_id': 3},
            {'id': 8, 'nombre': 'Retabilidad por categoria (Frescos)', 'unidad': '%', 'proceso_id': 3},
            {'id': 9, 'nombre': 'Retabilidad por categoria (Importados)', 'unidad': '%', 'proceso_id': 3},
            {'id': 10, 'nombre': 'Retabilidad por categoria (Inyectados)', 'unidad': '%', 'proceso_id': 3},
            {'id': 11, 'nombre': 'Rentabilidad por categoria (Procesados)', 'unidad': '%', 'proceso_id': 3},
            {'id': 12, 'nombre': 'Rentabilidad por categoria (Subproductos)', 'unidad': '%', 'proceso_id': 3},
            {'id': 13, 'nombre': 'Proporción Gasto Operativo', 'unidad': '%', 'proceso_id': 3},
            
            # Gestión Humana
            {'id': 14, 'nombre': 'Índice de rotación', 'unidad': '%', 'proceso_id': 4},
            {'id': 15, 'nombre': 'Índice de ausentismo', 'unidad': '%', 'proceso_id': 4},
            {'id': 16, 'nombre': '% Horas Extras', 'unidad': '%', 'proceso_id': 4},
            {'id': 17, 'nombre': 'Procesos disciplinarios', 'unidad': 'cantidad', 'proceso_id': 4},
            {'id': 18, 'nombre': 'Ausentismo', 'unidad': '%', 'proceso_id': 4},
            {'id': 19, 'nombre': 'Índice de satisfacción laboral', 'unidad': '%', 'proceso_id': 4},
            {'id': 20, 'nombre': '% Cumplimiento Gantt Proyecto GTH', 'unidad': '%', 'proceso_id': 4},
            
            # Planificación
            {'id': 21, 'nombre': 'Adherencia al plan de Produccion (LBS)', 'unidad': '%', 'proceso_id': 7},
            {'id': 22, 'nombre': 'Adherencia al plan de Produccion (Sacrificio)', 'unidad': '%', 'proceso_id': 7},
            {'id': 23, 'nombre': 'Adherencia al plan de Produccion (Deshuece)', 'unidad': '%', 'proceso_id': 7},
            {'id': 24, 'nombre': 'Rotación de existencia', 'unidad': '%', 'proceso_id': 7},
            
            # Producción
            {'id': 25, 'nombre': '% Adherencia Schedule planta ASD', 'unidad': '%', 'proceso_id': 8},
            {'id': 26, 'nombre': 'DESPERDICIO / SCRAP', 'unidad': '%', 'proceso_id': 8},
            {'id': 27, 'nombre': 'Porcentajes de reproceso', 'unidad': '%', 'proceso_id': 8},
            {'id': 28, 'nombre': 'Rendimiento Inyeccion - RES', 'unidad': '%', 'proceso_id': 8},
            {'id': 29, 'nombre': 'Rendimiento Inyeccion - CERDO', 'unidad': '%', 'proceso_id': 8},
            {'id': 30, 'nombre': 'Eficiencia de la Transformacion (LBS) / CERDO', 'unidad': '%', 'proceso_id': 8},
            
            # Ventas
            {'id': 31, 'nombre': 'Tasa de crecimiento de ventas', 'unidad': '%', 'proceso_id': 9},
            {'id': 32, 'nombre': 'Tasa de retención de clientes', 'unidad': '%', 'proceso_id': 9},
            {'id': 33, 'nombre': 'Rentabilidad por medio del mix', 'unidad': '%', 'proceso_id': 9},
            {'id': 34, 'nombre': 'Rentabilidad por vendedor', 'unidad': '%', 'proceso_id': 9},
        ]
        
        for i in indicadores:
            indicador = Indicador(id=i['id'], nombre=i['nombre'], unidad=i['unidad'], proceso_id=i['proceso_id'])
            db.session.add(indicador)
            
        db.session.commit()
        
        # Crear metas para 2025 (ejemplo parcial)
        metas = [
            # Administracion - ICE
            {'valor': 100.0, 'anio': 2025, 'mes': 1, 'indicador_id': 1},
            {'valor': 100.0, 'anio': 2025, 'mes': 2, 'indicador_id': 1},
            {'valor': 100.0, 'anio': 2025, 'mes': 3, 'indicador_id': 1},
            
            # Calidad - Quejas
            {'valor': 1.0, 'anio': 2025, 'mes': 1, 'indicador_id': 2},
            {'valor': 1.0, 'anio': 2025, 'mes': 2, 'indicador_id': 2},
            {'valor': 1.0, 'anio': 2025, 'mes': 3, 'indicador_id': 2},
            
            # Finanzas - Margen bruto
            {'valor': 23.5, 'anio': 2025, 'mes': 1, 'indicador_id': 5},
            {'valor': 23.5, 'anio': 2025, 'mes': 2, 'indicador_id': 5},
            {'valor': 24.0, 'anio': 2025, 'mes': 3, 'indicador_id': 5},
            
            # Finanzas - Ejecución presupuestaria
            {'valor': 100.0, 'anio': 2025, 'mes': 1, 'indicador_id': 6},
            {'valor': 100.0, 'anio': 2025, 'mes': 2, 'indicador_id': 6},
            {'valor': 100.0, 'anio': 2025, 'mes': 3, 'indicador_id': 6},
            
            # Producción - Adherencia Schedule
            {'valor': 100.0, 'anio': 2025, 'mes': 1, 'indicador_id': 25},
            {'valor': 100.0, 'anio': 2025, 'mes': 2, 'indicador_id': 25},
            {'valor': 100.0, 'anio': 2025, 'mes': 3, 'indicador_id': 25},
            
            # Ventas - Crecimiento
            {'valor': 10.0, 'anio': 2025, 'mes': 1, 'indicador_id': 31},
            {'valor': 10.0, 'anio': 2025, 'mes': 2, 'indicador_id': 31},
            {'valor': 10.0, 'anio': 2025, 'mes': 3, 'indicador_id': 31},
        ]
        
        for m in metas:
            meta = Meta(valor=m['valor'], anio=m['anio'], mes=m['mes'], indicador_id=m['indicador_id'])
            db.session.add(meta)
            
        db.session.commit()
        
        # Valores reales (ejemplo parcial)
        valores = [
            # Finanzas - Margen bruto
            {'valor': 22.0, 'anio': 2025, 'mes': 1, 'calificacion': 2.0, 'indicador_id': 5},
            {'valor': 20.0, 'anio': 2025, 'mes': 2, 'calificacion': 2.0, 'indicador_id': 5},
            
            # Finanzas - Ejecución presupuestaria
            {'valor': 95.74, 'anio': 2025, 'mes': 1, 'calificacion': 3.0, 'indicador_id': 6},
            {'valor': 96.52, 'anio': 2025, 'mes': 2, 'calificacion': 3.0, 'indicador_id': 6},
            
            # Ventas - Crecimiento
            {'valor': 4.0, 'anio': 2025, 'mes': 1, 'calificacion': 1.0, 'indicador_id': 31},
            {'valor': 24.0, 'anio': 2025, 'mes': 2, 'calificacion': 5.0, 'indicador_id': 31},
            
            # Producción - DESPERDICIO / SCRAP
            {'valor': 0.0, 'anio': 2025, 'mes': 1, 'calificacion': 1.0, 'indicador_id': 26},
            {'valor': 0.14, 'anio': 2025, 'mes': 2, 'calificacion': 5.0, 'indicador_id': 26},
            {'valor': 0.05, 'anio': 2025, 'mes': 3, 'calificacion': 5.0, 'indicador_id': 26},
            
            # Planificación - Adherencia LBS
            {'valor': 88.28, 'anio': 2025, 'mes': 2, 'calificacion': 2.0, 'indicador_id': 21},
            {'valor': 87.0, 'anio': 2025, 'mes': 3, 'calificacion': 2.0, 'indicador_id': 21},
        ]
        
        for v in valores:
            valor = Valor(valor=v['valor'], anio=v['anio'], mes=v['mes'], 
                         calificacion=v['calificacion'], indicador_id=v['indicador_id'])
            db.session.add(valor)
            
        db.session.commit()
        
        print("Datos iniciales cargados con éxito")

if __name__ == "__main__":
    poblar_datos_iniciales()