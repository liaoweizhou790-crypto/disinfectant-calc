const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
        AlignmentType, WidthType, Header, Footer, PageNumber, PageBreak } = require('docx');
const fs = require('fs');

// 创建规范公文文档
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "仿宋_GB2312", size: 32 }  // 三号字 = 16pt = 32 half-points
      }
    },
    paragraphStyles: [
      {
        id: "Title",
        name: "Title",
        basedOn: "Normal",
        next: "Normal",
        run: { size: 44, font: "方正小标宋简体" },  // 二号 = 22pt = 44 half-points
        paragraph: { 
          spacing: { line: 560, lineRule: "exact" },  // 固定值28磅
          alignment: AlignmentType.CENTER
        }
      },
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        run: { size: 32, bold: true, font: "黑体" },  // 三号黑体
        paragraph: { spacing: { line: 560, lineRule: "exact" } }
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        run: { size: 32, font: "楷体_GB2312" },  // 三号楷体不加粗
        paragraph: { spacing: { line: 560, lineRule: "exact" } }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },  // A4
        margin: { 
          top: 2098,    // 37mm = 2098 twips
          bottom: 1985, // 35mm = 1985 twips
          left: 1588,   // 28mm = 1588 twips (订口)
          right: 1474   // 26mm = 1474 twips
        }
      }
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: [PageNumber.CURRENT], font: "宋体", size: 24 })]  // 4号半角
        })]
      })
    },
    children: [
      // 发文机关标志（红头）- 模拟
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
        children: [new TextRun({ 
          text: "柳州市疾病预防控制中心文件", 
          bold: true,
          font: "方正小标宋简体",
          size: 44,
          color: "FF0000"  // 红色
        })]
      }),
      
      // 发文字号
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ 
          text: "柳疾控字〔2026〕5号", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 标题
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 560, lineRule: "exact", after: 400 },
        children: [new TextRun({ 
          text: "柳州市疾病预防控制中心关于审议《人工智能技术在消毒与病媒防制业务中的应用方案》（送审稿）的请示", 
          bold: true,
          font: "方正小标宋简体",
          size: 44  // 二号
        })]
      }),

      // 主送机关
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", after: 0 },
        children: [new TextRun({ 
          text: "市政府：", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 正文开头
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 200, after: 0 },
        indent: { firstLine: 640 },  // 首行缩进2字符（约640 twips）
        children: [new TextRun({ 
          text: "为深入贯彻落实国家疾控体系改革精神，积极推进疾控机构数字化转型，提升消毒与病媒生物防制业务技术水平，我所积极探索人工智能技术在疾控传统业务中的应用。现将《人工智能技术在消毒与病媒防制业务中的应用方案》（送审稿）呈上，请予审议。", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 一级标题：一、工作开展情况
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 200, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "一、工作开展情况", 
          bold: true,
          font: "黑体",
          size: 32
        })]
      }),

      // 二级标题：（一）平台建设
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 100, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "（一）AI智能助手平台建设", 
          font: "楷体_GB2312",
          size: 32
        })]
      }),

      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 100, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "引入OpenClaw智能代理网关平台，构建基于Agent架构的多渠道协同工作体系。实现飞书、微信等多渠道接入，支持文本、图片、文件等多种消息类型，数据本地存储符合疾控信息安全要求。", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 二级标题：（二）系统开发
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 200, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "（二）病原微生物防控系统开发", 
          font: "楷体_GB2312",
          size: 32
        })]
      }),

      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 100, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "自主开发V1.5.0版本，包含消毒剂配比计算、病原微生物智能识别（收录400+种病原）、AI流调分析等核心功能。基于《人间传染的病原微生物目录》（2023年版）和GB19193-2025标准开发，确保专业性和权威性。", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 二级标题：（三）DevOps建设
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 200, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "（三）GitHub DevOps自动化建设", 
          font: "楷体_GB2312",
          size: 32
        })]
      }),

      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 100, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "项目代码托管于GitHub平台，配置GitHub Actions工作流实现自动构建，每次代码推送自动触发APK构建，构建产物自动发布。", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 一级标题：二、应用成效
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 200, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "二、应用成效", 
          bold: true,
          font: "黑体",
          size: 32
        })]
      }),

      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 100, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "（一）业务效率显著提升。消毒剂配比计算从5-10分钟缩短至30秒，效率提升90%；流调报告分析实现AI辅助，效率提升70%。", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 100, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "（二）技术力量明显增强。借助AI知识库快速获取400+种病原微生物信息，专业化程度大幅提升；严格遵循国家标准，标准化水平显著提高。", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 100, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "（三）技术创新亮点突出。国内疾控系统率先引入OpenClaw AI代理平台，探索多Agent协同工作模式，实现多模态AI应用（文本、图片、PDF多格式分析）。", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 一级标题：三、下一步工作计划
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 200, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "三、下一步工作计划", 
          bold: true,
          font: "黑体",
          size: 32
        })]
      }),

      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 100, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "（一）短期目标（1-3个月）：完善多Agent架构，部署cdc Agent专属疾控业务代理，配置飞书路由规则实现业务分流；持续优化系统功能。", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 100, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "（二）中期目标（3-6个月）：实现AI模型本地化部署，保障高致病性病原数据安全；完善病媒监测数据库，对接现场监测设备。", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 100, after: 0 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "（三）长期目标（6-12个月）：实现全业务数字化转型，建设全所统一的业务数据中台；总结经验形成可复制的AI+疾控模式，在全市疾控系统推广应用。", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 结语
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 200, after: 400 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "妥否，请批示。", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 附件说明
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 200, after: 0 },
        indent: { firstLine: 640 },
        children: [
          new TextRun({ text: "附件：", bold: true, font: "仿宋_GB2312", size: 32 })
        ]
      }),
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 0, after: 0 },
        indent: { left: 640 },
        children: [new TextRun({ text: "1.《人工智能技术在消毒与病媒防制业务中的应用方案》（送审稿）", font: "仿宋_GB2312", size: 32 })]
      }),
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 0, after: 0 },
        indent: { left: 640 },
        children: [new TextRun({ text: "2. 柳州市病原微生物防控系统_v1.5.0.apk", font: "仿宋_GB2312", size: 32 })]
      }),
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 0, after: 400 },
        indent: { left: 640 },
        children: [new TextRun({ text: "3. 系统操作说明书", font: "仿宋_GB2312", size: 32 })]
      }),

      // 发文机关署名（右对齐）
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        spacing: { line: 560, lineRule: "exact", before: 400, after: 0 },
        indent: { right: 1134 },  // 右空4字
        children: [new TextRun({ 
          text: "柳州市疾病预防控制中心", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 成文日期
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        spacing: { line: 560, lineRule: "exact", before: 0, after: 400 },
        indent: { right: 1134 },
        children: [new TextRun({ 
          text: "2026年2月19日", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 附注（联系人）
      new Paragraph({
        spacing: { line: 560, lineRule: "exact", before: 200, after: 0 },
        children: [new TextRun({ 
          text: "（联系人：廖维洲  联系电话：XXXXXXX）", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 分页 - 附件
      new Paragraph({ children: [new PageBreak()] }),

      // 附件标题
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 560, lineRule: "exact", after: 400 },
        children: [new TextRun({ 
          text: "附件1", 
          bold: true,
          font: "黑体",
          size: 32
        })]
      }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 560, lineRule: "exact", after: 400 },
        children: [new TextRun({ 
          text: "人工智能技术在消毒与病媒防制业务中的应用方案", 
          bold: true,
          font: "方正小标宋简体",
          size: 44
        })]
      }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 560, lineRule: "exact", after: 600 },
        children: [new TextRun({ 
          text: "（送审稿）", 
          font: "仿宋_GB2312",
          size: 32
        })]
      }),

      // 附件正文
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { line: 560, lineRule: "exact", after: 400 },
        children: [new TextRun({ 
          text: "一、项目背景", 
          bold: true,
          font: "黑体",
          size: 32
        })]
      }),

      new Paragraph({
        spacing: { line: 560, lineRule: "exact", after: 200 },
        indent: { firstLine: 640 },
        children: [new TextRun({ 
          text: "（附件正文内容略，格式要求与正文相同）", 
          font: "仿宋_GB2312",
          size: 32
        })]
      })
    ]
  }]
});

// 生成文档
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/Users/liaoweizhou/.openclaw/workspace/请示_AI技术应用方案_2026年2月.docx", buffer);
  console.log("公文Word文档生成成功！");
});
