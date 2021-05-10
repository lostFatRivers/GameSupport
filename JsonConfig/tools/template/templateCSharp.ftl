using System.Collections.Generic;

namespace template
{
    /// <summary>
    /// ==================================<br/>
    /// = auto generated, do not modify! =<br/>
    /// ==================================
    /// </summary>
    public class ${className}
    {
        <#if fieldModelList??>
            <#list fieldModelList as fModel>
                <#if (fModel.fieldDesc)??>
        /// <summary>
        /// ${fModel.fieldDesc}
        /// </summary>
                </#if>
        public ${fModel.fieldType} ${fModel.fieldName} { get; set; }

            </#list>
        </#if>
    }
}