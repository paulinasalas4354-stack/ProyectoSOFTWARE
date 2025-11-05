import tkinter as tk
from tkinter import ttk, messagebox
from usuarios import Usuario
from dbUsuarios import dbUsuario
import re

def mostrar_interfaz_usuarios(ventana_menu_anterior, usuario_logueado):
    
    ventana_menu_anterior.withdraw()
    
    ventana = tk.Tk()
    ventana.title("Gestión de Usuarios - Sistema Escolar")
    ventana.geometry("700x550")

    modo_operacion = ""
    db = dbUsuario()

    # --- WIDGETS ---
    frame_principal = tk.Frame(ventana, padx=10, pady=10)
    frame_principal.pack(expand=True, fill=tk.BOTH)

    frame_busqueda = tk.LabelFrame(frame_principal, text="Búsqueda")
    frame_busqueda.pack(fill=tk.X, pady=5)
    tk.Label(frame_busqueda, text="Ingrese ID a buscar:").grid(row=0, column=0, padx=5, pady=5)
    entry_buscar = ttk.Entry(frame_busqueda, width=10)
    entry_buscar.grid(row=0, column=1, padx=5, pady=5)
    btn_buscar = ttk.Button(frame_busqueda, text="Buscar")
    btn_buscar.grid(row=0, column=2, padx=5, pady=5)

    frame_datos = tk.LabelFrame(frame_principal, text="Datos del Usuario")
    frame_datos.pack(fill=tk.BOTH, expand=True, pady=5)
    
    # --- Columna 0 (Etiquetas) ---
    tk.Label(frame_datos, text="ID:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
    tk.Label(frame_datos, text="Nombre:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
    tk.Label(frame_datos, text="A. Paterno:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
    tk.Label(frame_datos, text="A. Materno:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
    tk.Label(frame_datos, text="Email:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
    tk.Label(frame_datos, text="Username:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
    tk.Label(frame_datos, text="Password:").grid(row=6, column=0, sticky="w", padx=5, pady=2)
    tk.Label(frame_datos, text="Perfil:").grid(row=7, column=0, sticky="w", padx=5, pady=2)

    # --- Columna 1 (Campos de entrada) ---
    entry_id = ttk.Entry(frame_datos, state="disabled")
    entry_id.grid(row=0, column=1, sticky="we", padx=5, pady=2)
    
    entry_nombre = ttk.Entry(frame_datos)
    entry_nombre.grid(row=1, column=1, sticky="we", padx=5, pady=2)
    
    entry_apaterno = ttk.Entry(frame_datos)
    entry_apaterno.grid(row=2, column=1, sticky="we", padx=5, pady=2)
    
    entry_amaterno = ttk.Entry(frame_datos)
    entry_amaterno.grid(row=3, column=1, sticky="we", padx=5, pady=2)
    
    entry_email = ttk.Entry(frame_datos)
    entry_email.grid(row=4, column=1, sticky="we", padx=5, pady=2)
    
    entry_username = ttk.Entry(frame_datos)
    entry_username.grid(row=5, column=1, sticky="we", padx=5, pady=2)
    
    entry_password = ttk.Entry(frame_datos, show="*")
    entry_password.grid(row=6, column=1, sticky="we", padx=5, pady=2)

    combo_perfil = ttk.Combobox(frame_datos, 
                                values=["Administrador", "Maestro", "Alumno"], 
                                state="readonly") 
    combo_perfil.grid(row=7, column=1, sticky="we", padx=5, pady=2)

    frame_botones = tk.Frame(frame_principal)
    frame_botones.pack(fill=tk.X, pady=10)
    btn_nuevo = ttk.Button(frame_botones, text="Nuevo")
    btn_salvar = ttk.Button(frame_botones, text="Salvar")
    btn_cancelar = ttk.Button(frame_botones, text="Cancelar")
    btn_editar = ttk.Button(frame_botones, text="Editar")
    btn_remover = ttk.Button(frame_botones, text="Remover")
    btn_regresar = ttk.Button(frame_botones, text="Regresar al Menú")
    for i, btn in enumerate([btn_nuevo, btn_salvar, btn_cancelar, btn_editar, btn_remover, btn_regresar]):
        btn.grid(row=0, column=i, padx=5, pady=5)
        frame_botones.grid_columnconfigure(i, weight=1)

    # === FUNCIONES ===

    def validar_email(email):
        """Valida el formato del email"""
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email) is not None

    def validar_password(password):
        """Valida que la contraseña cumpla los requisitos"""
        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."
        
        if not re.search(r'[A-Z]', password):
            return False, "La contraseña debe contener al menos una mayúscula."
        
        if not re.search(r'[0-9]', password):
            return False, "La contraseña debe contener al menos un número."
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-]', password):
            return False, "La contraseña debe contener al menos un símbolo (!@#$%^&*...)."
        
        return True, ""

    def limpiar_campos():
        entry_id.config(state="normal")
        entry_id.delete(0, tk.END)
        entry_id.config(state="disabled")
        entry_nombre.delete(0, tk.END)
        entry_apaterno.delete(0, tk.END)
        entry_amaterno.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        combo_perfil.set("")
        entry_buscar.delete(0, tk.END)

    def configurar_estado_controles(estado):
        campos_edicion = [entry_nombre, entry_apaterno, entry_amaterno, 
                          entry_email, entry_username, entry_password, combo_perfil]
        
        if estado == "INICIO":
            for campo in campos_edicion: 
                campo.config(state="disabled")
            btn_nuevo.config(state="normal")
            btn_salvar.config(state="disabled")
            btn_cancelar.config(state="disabled")
            btn_editar.config(state="disabled")
            btn_remover.config(state="disabled")
            btn_buscar.config(state="normal")
            entry_buscar.config(state="normal")
        elif estado == "NUEVO" or estado == "EDITAR":
            for campo in campos_edicion: 
                campo.config(state="normal")
            btn_nuevo.config(state="disabled")
            btn_salvar.config(state="normal")
            btn_cancelar.config(state="normal")
            btn_editar.config(state="disabled")
            btn_remover.config(state="disabled")
            btn_buscar.config(state="disabled")
            entry_buscar.config(state="disabled")
        elif estado == "BUSCADO":
            for campo in campos_edicion: 
                campo.config(state="disabled")
            btn_nuevo.config(state="normal")
            btn_salvar.config(state="disabled")
            btn_cancelar.config(state="normal")
            btn_editar.config(state="normal")
            btn_remover.config(state="normal")
            btn_buscar.config(state="normal")
            entry_buscar.config(state="normal")
            
    def funcion_nuevo():
        nonlocal modo_operacion
        modo_operacion = "NUEVO"
        limpiar_campos()
        entry_id.config(state="normal")
        entry_id.insert(0, "(automático)")
        entry_id.config(state="disabled")
        combo_perfil.current(0) 
        configurar_estado_controles("NUEVO")
        entry_nombre.focus()

    def funcion_salvar():
        nonlocal modo_operacion
        
        # Obtener valores
        nombre = entry_nombre.get().strip()
        apaterno = entry_apaterno.get().strip()
        amaterno = entry_amaterno.get().strip()
        email = entry_email.get().strip()
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        perfil = combo_perfil.get().strip()

        # Validar campos vacíos
        if not nombre:
            messagebox.showwarning("Campo vacío", "Ingrese Nombre.")
            entry_nombre.focus()
            return
        if not apaterno:
            messagebox.showwarning("Campo vacío", "Ingrese Apellido Paterno.")
            entry_apaterno.focus()
            return
        if not amaterno:
            messagebox.showwarning("Campo vacío", "Ingrese Apellido Materno.")
            entry_amaterno.focus()
            return
        if not email:
            messagebox.showwarning("Campo vacío", "Ingrese Email.")
            entry_email.focus()
            return
        if not username:
            messagebox.showwarning("Campo vacío", "Ingrese Username.")
            entry_username.focus()
            return
        if not password:
            messagebox.showwarning("Campo vacío", "Ingrese Password.")
            entry_password.focus()
            return
        if not perfil:
            messagebox.showwarning("Campo vacío", "Seleccione Perfil.")
            combo_perfil.focus()
            return

        # Validar formato de email
        if not validar_email(email):
            messagebox.showerror("Email inválido", "Por favor ingrese un email válido (ejemplo@dominio.com)")
            entry_email.focus()
            return

        # Validar formato de contraseña
        password_valida, mensaje_error = validar_password(password)
        if not password_valida:
            messagebox.showerror("Contraseña débil", mensaje_error)
            entry_password.focus()
            return

        # Validar unicidad de username
        id_actual = entry_id.get()
        if modo_operacion == "EDITAR":
            if db.username_existe(username, excluir_id=int(id_actual)):
                messagebox.showerror("Dato Duplicado", f"El username '{username}' ya está en uso.")
                entry_username.focus()
                return
            if db.email_existe(email, excluir_id=int(id_actual)):
                messagebox.showerror("Dato Duplicado", f"El email '{email}' ya está registrado.")
                entry_email.focus()
                return
        else:  # NUEVO
            if db.username_existe(username):
                messagebox.showerror("Dato Duplicado", f"El username '{username}' ya está en uso.")
                entry_username.focus()
                return
            if db.email_existe(email):
                messagebox.showerror("Dato Duplicado", f"El email '{email}' ya está registrado.")
                entry_email.focus()
                return
        
        # Crear objeto Usuario
        usuario = Usuario()
        usuario.set_nombre(nombre)
        usuario.set_APaterno(apaterno)
        usuario.set_AMaterno(amaterno)
        usuario.set_email(email)
        usuario.set_username(username)
        usuario.set_password(password)
        usuario.set_perfil(perfil)

        if modo_operacion == "NUEVO":
            if db.crear_usuario(usuario):
                messagebox.showinfo("Éxito", f"Usuario '{nombre}' creado exitosamente.")
                limpiar_campos()
                configurar_estado_controles("INICIO")
        
        elif modo_operacion == "EDITAR":
            if not id_actual or not id_actual.isdigit():
                messagebox.showerror("Error", "No hay un ID de usuario válido para editar.")
                return
            
            usuario.set_usuario_id(int(id_actual))
            
            if db.editar_usuario(usuario):
                messagebox.showinfo("Éxito", f"Usuario '{nombre}' actualizado exitosamente.")
                limpiar_campos()
                configurar_estado_controles("INICIO")

    def funcion_buscar():
        id_a_buscar = entry_buscar.get().strip()
        if not id_a_buscar.isdigit():
            messagebox.showerror("ID Inválido", "El ID debe ser un número.")
            entry_buscar.focus()
            return
        
        usuario_encontrado = db.buscar_por_id(int(id_a_buscar))
        
        if usuario_encontrado:
            limpiar_campos()
            
            # Habilitar campos temporalmente para insertar
            campos_edicion = [entry_nombre, entry_apaterno, entry_amaterno, 
                              entry_email, entry_username, entry_password, combo_perfil]
            for campo in campos_edicion: 
                campo.config(state="normal")

            # Rellenar campos
            entry_id.config(state="normal")
            entry_id.insert(0, str(usuario_encontrado.get_usuario_id()))
            entry_id.config(state="disabled")
            entry_nombre.insert(0, usuario_encontrado.get_nombre())
            entry_apaterno.insert(0, usuario_encontrado.get_APaterno())
            entry_amaterno.insert(0, usuario_encontrado.get_AMaterno())
            entry_email.insert(0, usuario_encontrado.get_email())
            entry_username.insert(0, usuario_encontrado.get_username())
            entry_password.insert(0, usuario_encontrado.get_password())
            combo_perfil.set(usuario_encontrado.get_perfil())
            
            configurar_estado_controles("BUSCADO")
        else:
            messagebox.showinfo("No encontrado", f"No se encontró usuario con ID {id_a_buscar}.")
            limpiar_campos()

    def funcion_editar():
        nonlocal modo_operacion
        modo_operacion = "EDITAR"
        configurar_estado_controles("EDITAR")
        entry_nombre.focus()

    def funcion_remover():
        id_usuario = entry_id.get()
        if not id_usuario or not id_usuario.isdigit():
            messagebox.showerror("Error", "Busque un usuario válido para eliminar.")
            return
        
        nombre_usuario = entry_nombre.get()
        confirmar = messagebox.askyesno("Confirmar Eliminación", 
                                        f"¿Está seguro de eliminar al usuario?\n\n{nombre_usuario} (ID: {id_usuario})")
        
        if confirmar and db.eliminar_usuario(int(id_usuario)):
            messagebox.showinfo("Éxito", f"Usuario '{nombre_usuario}' eliminado exitosamente.")
            limpiar_campos()
            configurar_estado_controles("INICIO")

    def funcion_cancelar():
        nonlocal modo_operacion
        modo_operacion = ""  # Reiniciar modo de operación
        
        # Primero habilitar todos los campos para poder limpiarlos
        campos_edicion = [entry_nombre, entry_apaterno, entry_amaterno, 
                        entry_email, entry_username, entry_password, combo_perfil]
        for campo in campos_edicion: 
            campo.config(state="normal")
        
        # Ahora sí limpiar todos los campos
        limpiar_campos()
        
        # Finalmente configurar el estado inicial (que los deshabilita de nuevo)
        configurar_estado_controles("INICIO")

    def funcion_regresar():
        ventana.destroy()
        ventana_menu_anterior.deiconify()

    # === ASIGNACIÓN DE COMANDOS ===
    btn_nuevo.config(command=funcion_nuevo)
    btn_salvar.config(command=funcion_salvar)
    btn_buscar.config(command=funcion_buscar)
    btn_editar.config(command=funcion_editar)
    btn_remover.config(command=funcion_remover)
    btn_cancelar.config(command=funcion_cancelar)
    btn_regresar.config(command=funcion_regresar)

    # === ESTADO INICIAL ===
    configurar_estado_controles("INICIO")
    ventana.protocol("WM_DELETE_WINDOW", funcion_regresar)
    ventana.mainloop()
