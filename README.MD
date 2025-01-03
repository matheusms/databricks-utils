# Databricks Utility Notebooks for Unity Catalog  

This repository contains a collection of utility notebooks designed to facilitate and optimize operations within the Databricks Unity Catalog environment. These notebooks support tasks related to Delta Lake, Azure Synapse integration, workflow management, and Azure Data Factory (ADF) workflows.  

## Features  

### Workflow Management  

- **`ntb_disabling_workflows`**  
  Generates a table with the status of each workflow in the workspace:  
  - **Development (dev) or QA environments**: Disables workflows automatically.  
  - **Production (prd) environments**: Preserves the current status of workflows but logs their statuses in a table stored in Unity Catalog.  

- **`ntb_edit_permissions_wkl`**  
  Automatically updates the permissions of workflows:  
  - Assigns **Can View** permissions to a specified group.  
  - In dev environments, assigns **Can Manage** permissions to the group.  
  - In prd and qa environments, assigns **Can Manage Run** permissions to the group.  

### Delta Lake Utilities  

- **Deep Clone Operations**  
  Efficiently duplicate Delta tables, ensuring data consistency across environments.  

- **Sync Tables**  
  Automate table synchronization between environments or catalogs.  

### Azure Synapse Integration  

- **Schema Creation for External Tables**  
  Create and manage table schemas for external tables in Azure Synapse.  

### Azure Data Factory Integration  

- **ADF and Databricks Job Interactions**  
  Streamline integration and interaction between Azure Data Factory jobs and Databricks workflows.  

### Unity Catalog Management  

- **Table Ownership Management**  
  Modify table ownership within Unity Catalog to ensure appropriate access and governance.  