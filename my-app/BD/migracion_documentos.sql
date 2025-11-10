-- Script de migración para agregar tablas de documentos y notificaciones
-- Ejecutar este script si ya tienes la base de datos creada y quieres agregar las nuevas tablas

USE `crud_python`;

-- Volcando estructura para tabla crud_python.tbl_documentos
CREATE TABLE IF NOT EXISTS `tbl_documentos` (
  `id_documento` int NOT NULL AUTO_INCREMENT,
  `nombre_documento` varchar(100) NOT NULL,
  `fecha_vencimiento` date NOT NULL,
  `descripcion` text,
  `archivo_documento` mediumtext COMMENT 'Nombre del archivo PDF o imagen',
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_documento`),
  KEY `idx_fecha_vencimiento` (`fecha_vencimiento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando estructura para tabla crud_python.tbl_notificaciones_config
CREATE TABLE IF NOT EXISTS `tbl_notificaciones_config` (
  `id_config` int NOT NULL AUTO_INCREMENT,
  `id_documento` int NOT NULL,
  `dias_antes` int NOT NULL COMMENT 'Días antes del vencimiento para notificar (0=mismo día, 7=una semana, 30=un mes)',
  `notificar_mismo_dia` tinyint(1) DEFAULT 1 COMMENT '1=Notificar el mismo día, 0=No notificar',
  `notificar_una_semana` tinyint(1) DEFAULT 1 COMMENT '1=Notificar una semana antes, 0=No notificar',
  `notificar_un_mes` tinyint(1) DEFAULT 1 COMMENT '1=Notificar un mes antes, 0=No notificar',
  `notificado` tinyint(1) DEFAULT 0 COMMENT '0=No notificado, 1=Ya notificado',
  `fecha_notificacion` timestamp NULL DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_config`),
  KEY `idx_id_documento` (`id_documento`),
  KEY `idx_notificado` (`notificado`),
  CONSTRAINT `fk_notificaciones_documento` FOREIGN KEY (`id_documento`) REFERENCES `tbl_documentos` (`id_documento`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

