// Sistema de Notificaciones de Documentos

// Cargar notificaciones al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    cargarNotificaciones();
    // Recargar notificaciones cada 5 minutos
    setInterval(cargarNotificaciones, 300000);
});

// Función para cargar notificaciones
function cargarNotificaciones() {
    fetch('/api/notificaciones-pendientes')
        .then(response => response.json())
        .then(data => {
            if (data.notificaciones && data.notificaciones.length > 0) {
                mostrarNotificaciones(data.notificaciones);
                actualizarBadge(data.total);
            } else {
                mostrarSinNotificaciones();
                actualizarBadge(0);
            }
        })
        .catch(error => {
            console.error('Error al cargar notificaciones:', error);
            mostrarErrorNotificaciones();
        });
}

// Función para mostrar notificaciones
function mostrarNotificaciones(notificaciones) {
    const lista = document.getElementById('lista-notificaciones');
    const contador = document.getElementById('contador-notificaciones');
    
    if (!lista) return;
    
    contador.textContent = notificaciones.length;
    
    lista.innerHTML = '';
    
    notificaciones.forEach(notif => {
        const item = crearItemNotificacion(notif);
        lista.appendChild(item);
    });
}

// Función para crear un item de notificación
function crearItemNotificacion(notif) {
    const li = document.createElement('li');
    li.className = 'notification-item';
    
    // Determinar clase de color según el tipo
    let claseColor = 'text-primary';
    let icono = 'bi-file-earmark';
    
    if (notif.tipo === 'urgente' || notif.tipo === 'vencido') {
        claseColor = 'text-danger';
        icono = 'bi-exclamation-triangle-fill';
    } else if (notif.tipo === 'advertencia') {
        claseColor = 'text-warning';
        icono = 'bi-exclamation-circle-fill';
    } else {
        claseColor = 'text-info';
        icono = 'bi-info-circle-fill';
    }
    
    const fechaVencimiento = new Date(notif.fecha_vencimiento).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
    
    // Agregar evento para marcar como leída al hacer clic
    const link = document.createElement('a');
    link.className = 'dropdown-item';
    link.href = `/detalles-documento/${notif.id_documento}`;
    link.onclick = function() {
        // Marcar todas las notificaciones de este documento como leídas
        marcarTodasNotificacionesLeidas(notif.id_documento);
    };
    
    link.innerHTML = `
        <div class="d-flex">
            <div class="flex-shrink-0 me-3">
                <div class="avatar">
                    <span class="avatar-initial rounded-circle bg-label-${notif.tipo === 'urgente' || notif.tipo === 'vencido' ? 'danger' : notif.tipo === 'advertencia' ? 'warning' : 'primary'}">
                        <i class="bi ${icono}"></i>
                    </span>
                </div>
            </div>
            <div class="flex-grow-1">
                <h6 class="mb-1 ${claseColor}">${notif.mensaje}</h6>
                <p class="mb-0 text-muted small">Vence: ${fechaVencimiento}</p>
                <small class="text-muted">${notif.dias_restantes} días restantes</small>
            </div>
        </div>
    `;
    
    li.appendChild(link);
    return li;
}

// Función para mostrar mensaje cuando no hay notificaciones
function mostrarSinNotificaciones() {
    const lista = document.getElementById('lista-notificaciones');
    const contador = document.getElementById('contador-notificaciones');
    
    if (!lista) return;
    
    contador.textContent = '0';
    
    lista.innerHTML = `
        <li class="notification-item">
            <div class="text-center p-3">
                <i class="bi bi-check-circle text-success" style="font-size: 2rem;"></i>
                <p class="text-muted mb-0 mt-2">No hay notificaciones pendientes</p>
            </div>
        </li>
    `;
}

// Función para mostrar error
function mostrarErrorNotificaciones() {
    const lista = document.getElementById('lista-notificaciones');
    
    if (!lista) return;
    
    lista.innerHTML = `
        <li class="notification-item">
            <div class="text-center p-3">
                <i class="bi bi-exclamation-triangle text-warning" style="font-size: 2rem;"></i>
                <p class="text-muted mb-0 mt-2">Error al cargar notificaciones</p>
            </div>
        </li>
    `;
}

// Función para actualizar el badge de notificaciones
function actualizarBadge(cantidad) {
    const badge = document.getElementById('badge-notificaciones');
    
    if (!badge) return;
    
    if (cantidad > 0) {
        badge.textContent = cantidad > 99 ? '99+' : cantidad;
        badge.style.display = 'inline-block';
    } else {
        badge.style.display = 'none';
    }
}

// Función para marcar todas las notificaciones de un documento como leídas
function marcarTodasNotificacionesLeidas(idDocumento) {
    fetch('/api/marcar-todas-notificaciones-leidas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id_documento: idDocumento
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Recargar notificaciones después de un breve delay
            setTimeout(() => {
                cargarNotificaciones();
            }, 500);
        }
    })
    .catch(error => {
        console.error('Error al marcar notificaciones:', error);
    });
}

// Función para marcar notificación como leída (opcional, para uso futuro)
function marcarNotificacionLeida(idDocumento, diasAntes) {
    fetch('/api/marcar-notificacion-leida', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            id_documento: idDocumento,
            dias_antes: diasAntes
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Recargar notificaciones
            cargarNotificaciones();
        }
    })
    .catch(error => {
        console.error('Error al marcar notificación:', error);
    });
}

