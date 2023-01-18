USE project; 

DROP TABLE IF EXISTS [dbo].[#tmpFullJSONInfo]; 
DROP TABLE IF EXISTS [dbo].[covid_stats]; 
DROP TABLE IF EXISTS [dbo].[province]; 

SELECT [provCode], [provName], [stats]
INTO #tmpFullJSONInfo 
FROM OPENROWSET(BULK N'C:\project_files\covid_data.json', SINGLE_CLOB) AS dummydata 
	CROSS APPLY OPENJSON(bulkcolumn) 
WITH 
(
	[provCode]				VARCHAR(5) 				'$.code',				
	[provName]				VARCHAR(30)				'$.province',							
	[stats]					NVARCHAR(MAX)AS JSON 

);

ALTER TABLE #tmpFullJSONInfo alter column provCode VARCHAR(5) NOT NULL; 

SELECT	J.provCode, J.provName 
INTO Province 
FROM #tmpFullJSONInfo J; 

SELECT	IDENTITY(INT,1, 1) AS [csID], date_report, cases, cumulative_cases, J.provCode 
INTO	covid_stats 
FROM	#tmpFullJSONInfo J 
CROSS APPLY OPENJSON(J.stats) 
WITH
(
	[date_report]			VARCHAR(50),
	[cases]					BIGINT,
	[cumulative_cases]		BIGINT				
);

ALTER TABLE Province 
ADD CONSTRAINT PK_Province_provCode PRIMARY KEY (provCode); 

ALTER TABLE covid_stats 
ADD CONSTRAINT FK_PROVINCE_provCode FOREIGN KEY(provcode) REFERENCES PROVINCE(provcode); 