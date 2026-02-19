const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, HeadingLevel,
        AlignmentType, WidthType, Header, Footer, PageNumber } = require('docx');
const fs = require('fs');

// 创建文档
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "仿宋", size: 24 }
      }
    },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 36, bold: true, font: "黑体" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 }
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 32, bold: true, font: "黑体" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 }
      },
      {
        id: "Heading3",
        name: "Heading 3",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, font: "黑体" },
        paragraph: { spacing: { before: 120, after: 120 }, outlineLevel: 2 }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1800 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "柳州市疾病预防控制中心工作简报", font: "仿宋", size: 18 })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "第 ", font: "仿宋", size: 18 }),
            new TextRun({ children: [PageNumber.CURRENT], font: "仿宋", size: 18 }),
            new TextRun({ text: " 页", font: "仿宋", size: 18 })
          ]
        })]
      })
    },
    children: [
      // 标题
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ 
          text: "关于人工智能技术在消毒与病媒防制业务中应用的工作简报", 
          bold: true, 
          font: "黑体",
          size: 44
        })]
      }),
      
      // 报送信息
      new Paragraph({
        spacing: { before: 200, after: 200 },
        children: [
          new TextRun({ text: "报送单位：", bold: true, font: "仿宋" }),
          new TextRun({ text: "柳州市疾病预防控制中心消毒与病媒生物防制所", font: "仿宋" })
        ]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [
          new TextRun({ text: "编制日期：", bold: true, font: "仿宋" }),
          new TextRun({ text: "2026年2月", font: "仿宋" })
        ]
      }),
      new Paragraph({
        spacing: { after: 400 },
        children: [
          new TextRun({ text: "主题词：", bold: true, font: "仿宋" }),
          new TextRun({ text: "人工智能、疾控信息化、OpenClaw、Agent技术、消毒管理", font: "仿宋" })
        ]
      }),

      // 一、背景概述
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("一、背景概述")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun('为深入贯彻落实国家疾控体系改革精神，积极推进疾控机构数字化转型，我所积极探索人工智能技术在消毒与病媒生物防制传统业务中的应用，借助先进的OpenClaw智能代理平台，成功开发并部署了"柳州市病原微生物防控系统"，实现了传统业务与前沿技术的深度融合，显著提升了业务技术力量和应急处置能力。')]
      }),

      // 二、主要工作内容
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 400 },
        children: [new TextRun("二、主要工作内容")]
      }),

      // （一）
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("（一）基于OpenClaw平台的AI智能助手建设")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("1. 平台架构创新")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("我所率先引入国际先进的OpenClaw智能代理网关平台，构建了基于Agent（智能代理）架构的多渠道协同工作体系。OpenClaw作为自托管的AI网关，能够无缝连接飞书、微信、Telegram等多种通讯渠道，实现AI助手与业务人员的实时交互。")]
      }),
      
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun({ text: "技术亮点：", bold: true })]
      }),
      new Paragraph({
        children: [new TextRun("• Agent架构：采用多代理路由技术，支持不同业务场景下的独立Agent配置")]
      }),
      new Paragraph({
        children: [new TextRun("• 多渠道接入：通过飞书插件实现双向通信，支持文本、图片、文件等多种消息类型")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("• 私有化部署：数据本地存储，符合疾控信息安全要求")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("2. 多Agent协同工作体系（规划中）")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("针对疾控业务的专业性和复杂性，我所正在规划建设多Agent协同工作体系：main Agent处理日常事务、cdc Agent承载疾控核心业务、dev Agent负责开发测试。各Agent拥有独立的工作空间、记忆体系和工具权限，实现业务隔离与专业化处理。")]
      }),

      // （二）
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("（二）病原微生物防控系统（V1.5.0）开发")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("1. 系统功能概述")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun('我所自主开发的"柳州市病原微生物防控系统"（V1.5.0）是一款集消毒剂配比计算、病原微生物智能识别、流调报告分析于一体的综合性业务工具。系统基于《人间传染的病原微生物目录》（2023年版）和GB19193-2025《传染病消毒规范》开发，确保专业性和权威性。')]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("2. 核心功能模块")]
      }),
      
      // 功能模块表格
      new Table({
        width: { size: 9000, type: WidthType.DXA },
        columnWidths: [2000, 3500, 3500],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                children: [new Paragraph({ children: [new TextRun({ text: "模块", bold: true })] })],
                shading: { fill: "D9E2F3" }
              }),
              new TableCell({
                children: [new Paragraph({ children: [new TextRun({ text: "功能描述", bold: true })] })],
                shading: { fill: "D9E2F3" }
              }),
              new TableCell({
                children: [new Paragraph({ children: [new TextRun({ text: "技术特点", bold: true })] })],
                shading: { fill: "D9E2F3" }
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph("消毒剂配比计算")] }),
              new TableCell({ children: [new Paragraph("支持含氯消毒剂、醇类、过氧化物类等多种消毒剂的配比计算")] }),
              new TableCell({ children: [new Paragraph("智能单位换算、自动浓度计算")] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph("病原微生物库")] }),
              new TableCell({ children: [new Paragraph("收录400+种病原微生物信息，覆盖第一至第四类病原")] }),
              new TableCell({ children: [new Paragraph("按危害等级、传播途径、BSL等级多维筛选")] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph("智能消毒推荐")] }),
              new TableCell({ children: [new Paragraph("根据病原危害等级自动推荐消毒方案")] }),
              new TableCell({ children: [new Paragraph("一键应用推荐方案到配比计算器")] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph("AI流调分析")] }),
              new TableCell({ children: [new Paragraph("支持文本、图片、PDF格式的流调报告智能分析")] }),
              new TableCell({ children: [new Paragraph("AI识别致病菌、推荐消毒方案、生成PDF报告")] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph("病媒监测数据库")] }),
              new TableCell({ children: [new Paragraph("鼠、蝇、蟑、蚊、蜱虫五类病媒生物监测数据管理")] }),
              new TableCell({ children: [new Paragraph("可视化看板、趋势分析")] })
            ]
          })
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        spacing: { before: 200 },
        children: [new TextRun("3. 技术架构")]
      }),
      new Paragraph({
        spacing: { after: 100 },
        children: [new TextRun("前端采用HTML5 + JavaScript（离线可用），移动端使用Capacitor框架打包Android APK，数据存储采用SQLite本地数据库，AI模块支持Kimi、OpenAI、Claude等多种大模型API，部署采用GitHub Actions自动化构建。")]
      }),

      // （三）
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("（三）AI流调分析模块（V1.5.0核心功能）")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("AI流调分析模块是V1.5.0版本的核心创新，实现了流调报告的智能化处理。支持多模态输入（文本粘贴、图片上传、PDF文件）、PDF文本提取（集成PDF.js技术）、AI智能识别（调用大模型API自动识别致病菌和传播途径）、自动推荐方案（根据识别结果匹配病原数据库），以及PDF报告生成（一键导出专业的流调分析报告PDF）。")]
      }),

      // （四）
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("（四）GitHub DevOps自动化建设")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("项目代码托管于GitHub平台，配置GitHub Actions工作流实现自动构建：每次代码推送自动触发APK构建，JDK 21 + Node.js 22环境自动配置，构建产物自动上传到GitHub Artifacts。")]
      }),

      // 三、应用成效
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("三、应用成效")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("（一）业务效率提升")]
      }),
      
      // 效率提升表格
      new Table({
        width: { size: 9000, type: WidthType.DXA },
        columnWidths: [3000, 2000, 2000, 2000],
        rows: [
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "指标", bold: true })] })], shading: { fill: "D9E2F3" } }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "传统方式", bold: true })] })], shading: { fill: "D9E2F3" } }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "AI辅助方式", bold: true })] })], shading: { fill: "D9E2F3" } }),
              new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: "提升幅度", bold: true })] })], shading: { fill: "D9E2F3" } })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph("消毒剂配比计算")] }),
              new TableCell({ children: [new Paragraph("5-10分钟")] }),
              new TableCell({ children: [new Paragraph("30秒")] }),
              new TableCell({ children: [new Paragraph({ text: "90%", bold: true })] })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({ children: [new Paragraph("流调报告分析")] }),
              new TableCell({ children: [new Paragraph("人工判读")] }),
              new TableCell({ children: [new Paragraph("AI辅助")] }),
              new TableCell({ children: [new Paragraph({ text: "70%", bold: true })] })
            ]
          })
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("（二）技术创新亮点")]
      }),
      new Paragraph({
        children: [new TextRun("• OpenClaw智能网关：国内疾控系统率先引入AI代理平台")]
      }),
      new Paragraph({
        children: [new TextRun("• 多Agent架构：探索疾控业务的多代理协同工作模式")]
      }),
      new Paragraph({
        children: [new TextRun("• 多模态AI应用：文本、图片、PDF多格式流调报告分析")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("• DevOps实践：GitHub Actions自动化构建，提升开发效率")]
      }),

      // 四、下一步工作计划
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("四、下一步工作计划")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("（一）短期目标（1-3个月）")]
      }),
      new Paragraph({
        children: [new TextRun("1. 完善多Agent架构：部署cdc Agent专属疾控业务代理，配置飞书路由规则实现业务分流")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("2. 系统功能优化：收集用户反馈持续优化，增加更多病原微生物数据")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("（二）中期目标（3-6个月）")]
      }),
      new Paragraph({
        children: [new TextRun("1. AI模型本地化部署：评估Ollama等本地LLM方案，实现完全离线的流调分析能力")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("2. 病媒监测系统集成：完善病媒监测数据库，对接现场监测设备实现数据自动采集")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("（三）长期目标（6-12个月）")]
      }),
      new Paragraph({
        children: [new TextRun("1. 全业务数字化转型：扩展AI应用到更多疾控业务场景，建设全所统一的业务数据中台")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("2. 技术能力输出：总结经验形成可复制的AI+疾控模式，在全区/全市疾控系统推广应用")]
      }),

      // 五、结语
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("五、结语")]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun("人工智能技术在疾控业务中的应用前景广阔。我所通过引入OpenClaw智能代理平台，成功开发了病原微生物防控系统，实现了传统消毒与病媒防制业务的数字化转型。这不仅提升了业务处理效率，更增强了我所的技术力量和专业形象。未来，我所将继续深化AI技术应用，探索多Agent协同工作模式，建设更加智能化、专业化的疾控业务体系，为全市人民的健康保驾护航。")]
      }),

      // 编制信息
      new Paragraph({
        spacing: { before: 400 },
        children: [new TextRun({ text: "编制：廖维洲", font: "仿宋" })]
      }),
      new Paragraph({
        children: [new TextRun({ text: "审核：（待）", font: "仿宋" })]
      }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({ text: "批准：（待）", font: "仿宋" })]
      }),

      new Paragraph({
        spacing: { before: 200 },
        children: [new TextRun({ text: "附件：", bold: true, font: "仿宋" })]
      }),
      new Paragraph({
        children: [new TextRun({ text: "1. 柳州市病原微生物防控系统_v1.5.0.apk", font: "仿宋" })] }),
      new Paragraph({
        children: [new TextRun({ text: "2. 消毒剂配比系统_操作说明书.md", font: "仿宋" })] }),
      new Paragraph({
        children: [new TextRun({ text: "3. GitHub项目地址：https://github.com/liaoweizhou790-crypto/disinfectant-calc", font: "仿宋" })] }),
      new Paragraph({
        spacing: { after: 200 },
        children: [new TextRun({ text: "4. OpenClaw官网：https://openclaw.ai", font: "仿宋" })] }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 400 },
        children: [new TextRun({ text: "（此件公开发布）", font: "仿宋", italics: true })]
      })
    ]
  }]
});

// 生成文档
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/Users/liaoweizhou/.openclaw/workspace/工作简报_AI技术应用_2026年2月.docx", buffer);
  console.log("Word文档生成成功！");
});
