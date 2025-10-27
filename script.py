
import yaml

# Crear estructura YAML más completa y detallada para la presentación expandida
presentation_data_expanded = {
    "titulo_general": "Training General MRP para Gerencia de Disposición de Materiales AUDI",
    "total_slides": 35,
    "descripcion": "Programa de capacitación integral y detallado sobre Material Requirements Planning (MRP) en SAP",
    
    "modulos": [
        {
            "numero": 1,
            "titulo": "Fundamentos del MRP en SAP",
            "slides": [
                {
                    "slide_num": 1,
                    "titulo": "Tipos de MRP - Overview",
                    "contenido": {
                        "PD": {
                            "nombre": "MRP Planning",
                            "uso": "Demanda dependiente basada en MPS/PIRs",
                            "cuando_usar": "Productos con estructura BOM, producción planificada",
                            "ventajas": ["Explosión automática de BOMs", "Integración con producción"],
                            "desventajas": ["Requiere BOM actualizada", "Complejidad en multinivel"]
                        },
                        "VB": {
                            "nombre": "Manual Reorder Point Planning",
                            "uso": "Demanda independiente estable",
                            "cuando_usar": "Materiales de bajo costo, consumo predecible",
                            "ventajas": ["Simple de configurar", "Bajo mantenimiento"],
                            "desventajas": ["No considera BOM", "Manual setting de reorder point"]
                        },
                        "VV": {
                            "nombre": "Forecast-Based Planning",
                            "uso": "Basado en consumo histórico",
                            "cuando_usar": "Patrones de demanda estacionales",
                            "ventajas": ["Usa históricos", "Adaptable a tendencias"],
                            "desventajas": ["Requiere histórico confiable", "Sensible a cambios bruscos"]
                        },
                        "V1": {
                            "nombre": "Automatic Reorder Point",
                            "uso": "Cálculo automático de punto de reorden",
                            "cuando_usar": "Materiales C, optimización automática",
                            "ventajas": ["Cálculo automático", "Se ajusta dinámicamente"],
                            "desventajas": ["Menos control manual", "Requiere datos precisos"]
                        }
                    }
                },
                {
                    "slide_num": 2,
                    "titulo": "Lógica de Cálculo MRP - NETCH vs NETPL vs NEUPL",
                    "contenido": {
                        "NETCH": {
                            "nombre": "Net Change in Total Horizon",
                            "descripcion": "Solo materiales con cambios relevantes en planning file",
                            "horizonte": "Todo el horizonte futuro sin límite",
                            "performance": "Rápido - solo materiales modificados",
                            "uso_recomendado": "Ejecución diaria (nocturna)",
                            "ventajas": ["Eficiente", "Rápida ejecución", "Menor carga al sistema"],
                            "consideraciones": ["Depende de planning file entries", "Cambios fuera de horizonte si se consideran"]
                        },
                        "NETPL": {
                            "nombre": "Net Change in Planning Horizon",
                            "descripcion": "Solo materiales con cambios dentro del planning horizon",
                            "horizonte": "Limitado al planning horizon configurado (ej. 60-100 días)",
                            "performance": "Muy rápido - subset de NETCH",
                            "uso_recomendado": "Ejecuciones frecuentes intradiarias",
                            "ventajas": ["Más rápido que NETCH", "Enfoque en corto plazo"],
                            "riesgos": ["Cambios fuera del horizonte no se consideran", "Puede perder requirements lejanos"]
                        },
                        "NEUPL": {
                            "nombre": "Regenerative Planning",
                            "descripcion": "Todos los materiales independiente de cambios",
                            "horizonte": "Completo sin restricción",
                            "performance": "Lento - procesa todos los materiales",
                            "uso_recomendado": "Semanal (lunes) o mensual",
                            "ventajas": ["Limpia planned orders obsoletos", "Refresh completo", "Elimina 'aged in place' orders"],
                            "cuando_ejecutar": ["Inicio de semana/mes", "Después de cambios masivos en maestros", "Go-live inicial"]
                        }
                    }
                },
                {
                    "slide_num": 3,
                    "titulo": "Parámetros Principales del MRP",
                    "contenido": {
                        "Planning_Time_Fence": {
                            "definicion": "Período protegido donde MRP no hace cambios automáticos",
                            "zonas": {
                                "Firm_Zone": "Órdenes released - no modificables por MRP",
                                "Slushy_Zone": "Planned orders - cambios limitados",
                                "Outside_Fence": "MRP tiene libertad completa"
                            },
                            "configuracion": "MRP 1 view - Planning Time Fence field (días)",
                            "ejemplo_audi": "PTF = 10 días - primeros 10 días congelados"
                        },
                        "Horizonte_Planeacion": {
                            "definicion": "Período futuro para el cual MRP calcula requirements",
                            "configuracion": "MRP Group o Plant level",
                            "tipico": "60-120 días workdays",
                            "formula": "Horizonte = Current Date + Planning Horizon Days"
                        },
                        "Stock_Seguridad": {
                            "definicion": "Cantidad buffer contra variabilidad de demanda",
                            "ubicacion": "MRP 2 view - Safety Stock field",
                            "consideracion": "No disponible para MRP (buffer permanente)"
                        }
                    }
                },
                {
                    "slide_num": 4,
                    "titulo": "Transacciones MD04 vs MD03 vs MD05",
                    "comparacion": {
                        "MD04": {
                            "nombre": "Stock/Requirements List",
                            "tipo": "Dinámico - tiempo real",
                            "actualizacion": "Inmediata con cada transacción",
                            "uso": "Análisis diario, troubleshooting en vivo",
                            "columnas_clave": ["MRP element", "Receipt/Requirement", "Date", "Available qty", "Exception msg"],
                            "ventajas": ["Siempre actualizado", "Refleja situación real", "Drill-down a documentos"],
                            "cuando_usar": "Análisis diario de disponibilidad y acciones inmediatas"
                        },
                        "MD05": {
                            "nombre": "MRP List",
                            "tipo": "Estático - snapshot del último MRP run",
                            "actualizacion": "Solo con nuevo MRP run",
                            "uso": "Análisis de resultados de planificación",
                            "columnas_clave": ["Planning element", "Exception messages", "Action required", "Proposed dates"],
                            "ventajas": ["Muestra qué decidió MRP", "Histórico de planning runs", "Exception messages claros"],
                            "cuando_usar": "Post-MRP analysis, validación de lógica de planificación"
                        },
                        "MD03": {
                            "nombre": "Display Planning Data",
                            "tipo": "Display de datos maestros y situación",
                            "contenido": ["Planning data from master", "Current stock situation", "Overview sin drill-down"],
                            "uso": "Vista rápida de datos de planificación",
                            "cuando_usar": "Verificación rápida de configuración y situación"
                        }
                    }
                },
                {
                    "slide_num": 5,
                    "titulo": "Planning Time Fence - Zonas de Control",
                    "contenido": {
                        "concepto": "Período que estabiliza el plan de corto plazo evitando cambios automáticos",
                        "zones_detail": {
                            "Inside_Firm_Zone": {
                                "periodo": "0 - Release period (típico 0-5 días)",
                                "ordenes": "Released orders, Production orders, Purchase orders firmes",
                                "comportamiento_mrp": "MRP NO modifica - solo exception messages",
                                "accion_planificador": "Cambios 100% manuales"
                            },
                            "Slushy_Zone": {
                                "periodo": "Release period - PTF (típico 5-10 días)",
                                "ordenes": "Planned orders, Requisiciones",
                                "comportamiento_mrp": "MRP modifica con restricciones",
                                "accion_planificador": "Revisar cambios propuestos"
                            },
                            "Outside_Fence": {
                                "periodo": "Después del PTF (10+ días)",
                                "ordenes": "Planned orders futuros",
                                "comportamiento_mrp": "Libertad completa - create/delete/reschedule",
                                "accion_planificador": "Monitoreo periódico"
                            }
                        },
                        "configuracion_audi": {
                            "PTF_tipico": "10 días workdays",
                            "Opening_period": "5 días (PRs en vez de planned orders)",
                            "estrategia": "Estabilidad en ventana de 2 semanas"
                        }
                    }
                }
            ]
        },
        {
            "numero": 2,
            "titulo": "Datos Maestros de Planeación",
            "slides": [
                {
                    "slide_num": 6,
                    "titulo": "Vistas MRP del Maestro de Materiales",
                    "vistas": {
                        "MRP_1": {
                            "campos_criticos": {
                                "MRP_Type": "PD, VB, VV, V1 - determina lógica de planificación",
                                "MRP_Controller": "Responsable del material (ej. 001, 002)",
                                "Lot_Size": "EX, FX, HB - procedimiento de tamaño de lote",
                                "Procurement_Type": "E (External), F (In-house), X (Both)",
                                "Planning_Time_Fence": "Días de congelación",
                                "ABC_Indicator": "A (crítico), B (importante), C (bajo valor)"
                            }
                        },
                        "MRP_2": {
                            "campos_criticos": {
                                "Safety_Stock": "Cantidad física de buffer",
                                "Safety_Time": "Días adicionales de lead time",
                                "Min_Safety_Stock": "Límite inferior",
                                "Service_Level": "% (ej. 95%, 99%)",
                                "Plan_Delivery_Time": "Días de entrega del proveedor",
                                "GR_Processing_Time": "Días de proceso de recepción",
                                "Availability_Check": "Grupo de verificación (01, 02)"
                            }
                        },
                        "MRP_3": {
                            "campos_criticos": {
                                "Strategy_Group": "Estrategia de planificación (10, 11, 40)",
                                "Consumption_Mode": "Forward, Backward, Forward/Backward",
                                "Consumption_Period": "Días para consumption"
                            }
                        },
                        "MRP_4": {
                            "campos_criticos": {
                                "REM_Profile": "Repetitive manufacturing",
                                "Storage_Costs": "Para lot size optimization",
                                "Individual_Collective": "Requisitos individuales o colectivos"
                            }
                        }
                    }
                },
                {
                    "slide_num": 7,
                    "titulo": "Safety Stock vs Safety Time - Análisis Comparativo",
                    "comparacion_detallada": {
                        "Safety_Stock": {
                            "naturaleza": "Buffer de CANTIDAD física",
                            "ubicacion_mm": "MRP 2 view - Safety Stock field",
                            "proposito": "Protección contra variabilidad de DEMANDA",
                            "formula_sap": "SS = R × √W × MAD",
                            "componentes_formula": {
                                "R": "Safety factor (del service level - ej. 95% = 1.65, 99% = 2.33)",
                                "W": "Replenishment Lead Time en períodos",
                                "MAD": "Mean Absolute Deviation (precisión de forecast)"
                            },
                            "comportamiento_mrp": "NO disponible para planificación - permanece como buffer",
                            "efecto_inventario": "AUMENTA el nivel de inventario físico",
                            "cuando_usar": "Alta variabilidad en demanda, productos críticos A",
                            "ejemplo_audi": "Motor 2.0T: SS = 50 unidades para cubrir spikes de demanda"
                        },
                        "Safety_Time": {
                            "naturaleza": "Buffer de TIEMPO (días)",
                            "ubicacion_mm": "MRP 2 view - Safety Time/Actual Range of Coverage field",
                            "proposito": "Protección contra variabilidad de SUMINISTRO (delays)",
                            "mecanismo": "Adelanta fechas de requirements simulativamente",
                            "comportamiento_mrp": "Requirement de 30-Mar se planea como 28-Mar (si ST=2 días)",
                            "efecto_inventario": "Puede aumentar inventario temporalmente por adelanto",
                            "cuando_usar": "Proveedores con variabilidad en lead time, transporte internacional",
                            "ejemplo_audi": "Componentes importados: ST = 3 días para cubrir delays aduanales",
                            "options": {
                                "indicator_1": "Solo para independent requirements",
                                "indicator_2": "Para todos los requirements"
                            }
                        }
                    },
                    "decision_matrix": {
                        "problema_demanda": "Use Safety Stock",
                        "problema_suministro": "Use Safety Time",
                        "ambos_problemas": "Combinar Safety Stock + Safety Time",
                        "costo_inventario_critico": "Preferir Safety Time"
                    }
                },
                {
                    "slide_num": 8,
                    "titulo": "Lead Times - Plan Delivery Time vs GR Processing Time",
                    "contenido": {
                        "Plan_Delivery_Time": {
                            "definicion": "Tiempo desde emisión de PO hasta llegada física del material",
                            "ubicacion": "MRP 2 view - Planned Deliv. Time field",
                            "unidad": "Calendar days",
                            "incluye": ["Tiempo de fabricación del proveedor", "Tiempo de transporte", "Buffer del proveedor"],
                            "no_incluye": "Procesamiento interno post-recepción",
                            "ejemplo": "Proveedor en Alemania a planta México: 21 días"
                        },
                        "GR_Processing_Time": {
                            "definicion": "Tiempo interno desde llegada física hasta disponibilidad en stock",
                            "ubicacion": "MRP 2 view - GR Processing Time field",
                            "unidad": "Workdays",
                            "incluye": ["Descarga", "Inspección de calidad", "Put-away al warehouse", "Posteo en sistema"],
                            "ejemplo": "Inspección QA + almacenaje: 2 días"
                        },
                        "Total_Lead_Time": {
                            "formula": "Total LT = Plan Delivery Time + GR Processing Time",
                            "ejemplo_calculo": "21 días + 2 días = 23 días total",
                            "uso_mrp": "MRP calcula order date = Requirement date - Total LT",
                            "consideracion": "PDT en calendar days, GRPT en workdays - conversión automática"
                        },
                        "In_House_Production_Time": {
                            "definicion": "Para materiales tipo F (in-house production)",
                            "ubicacion": "MRP 2 view - In-house production field",
                            "incluye": ["Setup time", "Production time", "Queue time", "Move time"]
                        }
                    }
                },
                {
                    "slide_num": 9,
                    "titulo": "Lot Sizing Procedures - Procedimientos de Tamaño de Lote",
                    "procedimientos_estaticos": {
                        "EX": {
                            "nombre": "Exact Lot Size (Lot-for-Lot)",
                            "comportamiento": "Cantidad de orden = Cantidad de requirement EXACTA",
                            "formula": "Order Qty = Requirement Qty",
                            "ejemplo": "Requirement 127 kg → Order 127 kg",
                            "ventajas": ["Sin inventario excess", "Flexible", "Responde exacto a demanda"],
                            "desventajas": ["Muchas órdenes pequeñas", "Altos costos administrativos"],
                            "cuando_usar": "Items A, productos terminados, demanda variable"
                        },
                        "FX": {
                            "nombre": "Fixed Lot Size",
                            "comportamiento": "Múltiplos de cantidad fija configurada",
                            "configuracion": "MRP 1 view - Fixed Lot Size field",
                            "ejemplo": "Fixed Lot = 250, Req = 600 → 3 orders de 250 (750 total)",
                            "ventajas": ["Packing standards", "Full truck loads", "MOQ management"],
                            "desventajas": ["Inventario excess", "Menos flexible"],
                            "cuando_usar": "MOQ de proveedores, full containers, pallet quantities"
                        },
                        "HB": {
                            "nombre": "Replenish to Maximum Stock Level",
                            "comportamiento": "Llenar hasta Max Stock Level",
                            "formula": "Order Qty = Max Stock - Current Stock - Fixed Receipts + Total Requirements",
                            "configuracion": "MRP 1: Lot Size = HB; MRP 3: Max Stock Level",
                            "ejemplo": "Max=5000, Current=1000, Req=4000 → Order 8000",
                            "cuando_usar": "Tanques, silos, gas, líquidos a granel"
                        }
                    },
                    "procedimientos_periodicos": {
                        "WB": {
                            "nombre": "Weekly Lot Size",
                            "comportamiento": "Agrupa requirements de 1 semana",
                            "ejemplo": "Lun: 100, Mie: 150, Vie: 200 → 1 order por 450 al inicio de semana"
                        },
                        "MB": {
                            "nombre": "Monthly Lot Size",
                            "comportamiento": "Agrupa requirements de 1 mes"
                        }
                    },
                    "parametros_adicionales": {
                        "Minimum_Lot_Size": "Cantidad mínima a ordenar",
                        "Maximum_Lot_Size": "Cantidad máxima por orden",
                        "Rounding_Value": "Redondeo (ej. múltiplos de 10)",
                        "Assembly_Scrap": "% de scrap esperado en producción"
                    }
                },
                {
                    "slide_num": 10,
                    "titulo": "Bill of Materials (BOM) - Estructura y Consulta",
                    "conceptos": {
                        "definicion": "Lista estructurada de todos los componentes necesarios para fabricar un producto",
                        "niveles": {
                            "Level_0": "Finished Product (FG)",
                            "Level_1": "Subassemblies directs",
                            "Level_2_N": "Components y raw materials"
                        }
                    },
                    "transacciones_bom": {
                        "CS01": {
                            "funcion": "Create Material BOM",
                            "uso": "Crear nueva estructura de producto"
                        },
                        "CS02": {
                            "funcion": "Change Material BOM",
                            "uso": "Modificar BOM existente"
                        },
                        "CS03": {
                            "funcion": "Display Material BOM - Single Level",
                            "uso": "Ver estructura un nivel (header + componentes directos)",
                            "info_mostrada": ["Item number", "Component", "Quantity", "Unit", "Item category (L,N,R)", "Change numbers"],
                            "cuando_usar": "Verificación rápida de componentes de primer nivel"
                        },
                        "CS11": {
                            "funcion": "Material BOM - Multi-Level (Level by Level)",
                            "uso": "Explosión completa nivel por nivel",
                            "ventajas": "Ve estructura completa jerárquica",
                            "ejemplo": "FG → Subassembly A → Component X, Y, Z"
                        },
                        "CS12": {
                            "funcion": "Material BOM - Multi-Level with quantities",
                            "uso": "Como CS11 pero con cantidades acumuladas",
                            "ejemplo": "Si Level 1 usa 2 de Subassembly y Subassembly usa 3 de Component X → Total = 6 Component X por FG"
                        },
                        "CS13": {
                            "funcion": "Summarized BOM",
                            "uso": "Lista consolidada de todos los componentes sin jerarquía",
                            "ventajas": "Vista flat de materials necesarios"
                        },
                        "CS15": {
                            "funcion": "BOM Usage - Where Used List",
                            "uso": "Encontrar en qué productos se usa un componente",
                            "ejemplo": "Component X usado en: Product A, Product B, Product C",
                            "aplicacion": "Engineering changes, obsolescence planning"
                        }
                    },
                    "demanda_dependiente": {
                        "concepto": "Demand que se deriva de demanda de nivel superior",
                        "ejemplo": "10 units de Vehicle (Level 0) → 40 units de Wheel (Level 1, qty=4 per vehicle)",
                        "mrp_behavior": "MRP explota BOM y crea dependent requirements automáticamente",
                        "importante": "Dependent requirements NO son sales orders - son calculados por MRP"
                    }
                }
            ]
        },
        {
            "numero": 3,
            "titulo": "Monitoreo de Excepciones y Análisis",
            "slides": [
                {
                    "slide_num": 11,
                    "titulo": "Exception Messages - Códigos y Acciones",
                    "categorias": {
                        "New_Order_Proposals": {
                            "msg_1": {
                                "codigo": "1",
                                "mensaje": "Newly created order proposal",
                                "significado": "MRP creó nueva orden en este run",
                                "accion": "Informativo - revisar si es esperado",
                                "prioridad": "Media"
                            },
                            "msg_2": {
                                "codigo": "2",
                                "mensaje": "New, opening date in the past",
                                "significado": "Nueva orden con opening date ya pasado",
                                "accion": "Cambiar opening date o expedite",
                                "prioridad": "Alta"
                            },
                            "msg_3": {
                                "codigo": "3",
                                "mensaje": "New, start date in the past",
                                "significado": "Start date ya pasó",
                                "accion": "Reschedule o expedite urgente",
                                "prioridad": "Crítica"
                            },
                            "msg_4": {
                                "codigo": "4",
                                "mensaje": "New, finish date in the past",
                                "significado": "Finish date en pasado - shortage inminente",
                                "accion": "Acción inmediata - expedite o buscar alternativa",
                                "prioridad": "Crítica"
                            }
                        },
                        "Rescheduling_Messages": {
                            "msg_5": {
                                "codigo": "5",
                                "mensaje": "Opening date in the past",
                                "significado": "Orden existente con opening date pasado",
                                "accion": "Update dates",
                                "prioridad": "Media"
                            },
                            "msg_6": {
                                "codigo": "6",
                                "mensaje": "Start date in the past",
                                "significado": "Start date pasado",
                                "accion": "Reschedule",
                                "prioridad": "Alta"
                            },
                            "msg_7": {
                                "codigo": "7",
                                "mensaje": "Finish date in the past",
                                "significado": "Finish date pasado",
                                "accion": "Expedite",
                                "prioridad": "Crítica"
                            },
                            "msg_10": {
                                "codigo": "10",
                                "mensaje": "Reschedule in",
                                "significado": "Receipt puede moverse hacia adelante (más tarde)",
                                "accion": "Posponer orden para liberar capacidad",
                                "prioridad": "Baja"
                            },
                            "msg_15": {
                                "codigo": "15",
                                "mensaje": "Reschedule out",
                                "significado": "Receipt debe adelantarse (más temprano)",
                                "accion": "Adelantar fecha de entrega con proveedor",
                                "prioridad": "Alta"
                            }
                        },
                        "Cancel_Messages": {
                            "msg_20": {
                                "codigo": "20",
                                "mensaje": "Cancel process",
                                "significado": "Proposal no es necesario - demand cancelada",
                                "accion": "Cancelar orden o convertir a stock",
                                "prioridad": "Media"
                            }
                        },
                        "Stock_Messages": {
                            "msg_25": {
                                "codigo": "25",
                                "mensaje": "Excess stock",
                                "significado": "Stock planeado excede máximo",
                                "accion": "Reducir órdenes futuras o usar excess",
                                "prioridad": "Media"
                            },
                            "msg_56": {
                                "codigo": "56",
                                "mensaje": "Shortage in planning time fence",
                                "significado": "Faltante en período congelado",
                                "accion": "Acción manual urgente - split de órdenes",
                                "prioridad": "Crítica"
                            },
                            "msg_96": {
                                "codigo": "96",
                                "mensaje": "Stock fallen below safety stock",
                                "significado": "Nivel de safety stock penetrado",
                                "accion": "Expedite procurement",
                                "prioridad": "Alta"
                            }
                        },
                        "BOM_Messages": {
                            "msg_50": {
                                "codigo": "50",
                                "mensaje": "No BOM exists",
                                "significado": "Material no tiene BOM",
                                "accion": "Crear BOM o cambiar MRP type",
                                "prioridad": "Crítica"
                            },
                            "msg_52": {
                                "codigo": "52",
                                "mensaje": "No BOM selected",
                                "significado": "BOM existe pero no se seleccionó",
                                "accion": "Revisar BOM usage, validity dates",
                                "prioridad": "Alta"
                            }
                        }
                    },
                    "transaccion_config": "OMD3 - Configuración de exception messages"
                }
            ]
        }
    ]
}

# Guardar en formato YAML
yaml_string = yaml.dump(presentation_data_expanded, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120)

# Mostrar una muestra
print("=" * 80)
print("ESTRUCTURA YAML COMPLETA PARA PRESENTACIÓN EXPANDIDA")
print("=" * 80)
print(f"\nTotal de slides planeados: {presentation_data_expanded['total_slides']}")
print(f"Total de módulos: {len(presentation_data_expanded['modulos'])}")
print("\n" + yaml_string[:2000])
print("\n... [Contenido adicional disponible] ...")
